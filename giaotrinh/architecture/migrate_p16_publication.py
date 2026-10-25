"""Reconcile the new Part XVI with publication metadata after authoring edits.

Historical P15.C04 content and QA are immutable input in history_p15_c04.
This script never changes P01–P15 lessons and never renders the PDF.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "architecture/history_p15_c04"


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8")


def main():
    tree = read(ROOT / "architecture/knowledge_tree.json")
    mapping = read(ROOT / "architecture/p15_c04_to_p16.json")["lesson_map"]
    old = read(ARCHIVE / "manifest_rows.json")
    old_sources = read(ARCHIVE / "source_map.json")["sources"]
    source_map = read(ROOT / "manuscript/P16/source_map.json")
    for sid, source in old_sources.items():
        if source_map["sources"].get(sid, {}).get("url") != source["url"]:
            raise ValueError(f"historical source URL changed: {sid}")
    lock = ROOT / "manuscript/P16/source_ids.lock.json"
    urls = {sid: item["url"] for sid, item in source_map["sources"].items()}
    if lock.exists():
        locked = read(lock)["urls"]
        for sid, url in locked.items():
            if urls.get(sid) != url:
                raise ValueError(f"published P16 source identity changed: {sid}")
    else:
        write(lock, {"schema_version": 1, "urls": urls})

    manifest_path = ROOT / "manuscript/manifest.json"
    manifest = read(manifest_path)
    manifest["lessons"] = {k: v for k, v in manifest["lessons"].items()
                           if not k.startswith("P15.C04.")}
    new_qa = read(ROOT / "manuscript/P16/qa.json")
    reverse = {entry["primary"]: old_id for old_id, entry in mapping.items()}
    titles_path = ROOT / "manuscript/exercise_titles.json"
    titles = {k: v for k, v in read(titles_path).items()
              if not k.startswith("P15.C04.")}
    reader_path = ROOT / "manuscript/reader_titles.json"
    reader = read(reader_path)
    for category in ("chapters", "lessons"):
        reader[category] = {k: v for k, v in reader[category].items()
                            if not k.startswith("P15.C04")}
    reader["parts"]["P16"] = "Tư duy kiến trúc và tích hợp hệ sinh thái DevOps"
    reader["chapters"].pop("P15.C04", None)

    claims_by_lesson: dict[str, set[str]] = {}
    for claim in source_map["claims"]:
        lid = claim["lesson"]
        claims_by_lesson.setdefault(lid, set()).update(claim["sources"])
    count = 0
    for part in tree["parts"]:
        if part["id"] != "P16":
            continue
        for chapter in part["chapters"]:
            reader["chapters"][chapter["id"]] = chapter["title"]
            for lesson in chapter["lessons"]:
                lid = lesson["id"]
                relative = "manuscript/" + lid.replace(".", "/") + ".md"
                body = (ROOT / relative).read_text(encoding="utf-8")
                if len(body.split()) < 100:
                    raise ValueError(f"lesson incomplete: {lid}")
                if lid in reverse:
                    previous = old["lessons"][reverse[lid]]["qa"][0]
                    title = old["exercise_titles"][reverse[lid] + ".Q01"]
                    question, answer = previous["question"], previous["answer"]
                else:
                    item = new_qa[lid]
                    title, question, answer = (item[k] for k in
                                               ("title", "question", "answer"))
                qid = lid + ".Q01"
                titles[qid] = title
                row = {
                    "parent": chapter["id"],
                    "prerequisites": lesson["prerequisites"],
                    "status": "reviewed",
                    "verification": "author_verified_p16",
                    "editorial_override": True,
                    "content": relative,
                    "sha256": hashlib.sha256(body.strip().encode("utf-8")).hexdigest(),
                    "legacy_units": [],
                    "claim_ids": [],
                    "examples": [],
                    "source_ids": sorted(claims_by_lesson.get(lid, set())),
                    "qa": [{"id": qid, "publication_id": qid,
                            "question": question, "answer": answer}],
                }
                manifest["lessons"][lid] = row
                reader["lessons"][lid] = lesson["title"]
                count += 1
    if count != 24 or len(manifest["lessons"]) != 202:
        raise ValueError(f"migration incomplete: {count} P16 / "
                         f"{len(manifest['lessons'])} total")
    manifest["phase"] = "part16_author_verified_candidate"
    write(manifest_path, manifest)
    write(reader_path, reader)
    write(titles_path, titles)

    cross_path = ROOT / "manuscript/cross_references.json"
    cross = read(cross_path)
    cross["sources"] = {k: v for k, v in cross["sources"].items()
                        if "P15.C04" not in k and all("P15.C04" not in dest for dest in v)}
    cross["sources"]["lesson:P16.C01.L01"] = ["P15.C03"]
    write(cross_path, cross)
    print(f"P16_MIGRATED lessons={count} total={len(manifest['lessons'])} "
          f"sources={len(urls)}")


if __name__ == "__main__":
    main()
