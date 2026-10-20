"""One-time, ledger-checked migration of the reviewed manuscript into stable lesson IDs.

The old chapters remain immutable evidence. Run this script again only after
reviewing the resulting diff; it refuses to overwrite edited lesson files.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCH = ROOT / "architecture"
OUT = ROOT / "manuscript"


def rows(name: str) -> list[dict[str, str]]:
    with (ARCH / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def sections(path: Path) -> tuple[str, dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    first = re.search(r"(?m)^## \d+\.\d+\. ", text)
    if first is None:
        raise ValueError(f"No numbered sections: {path}")
    intro = text[:first.start()].split("\n", 1)[-1].strip()
    found: dict[str, str] = {}
    for match in re.finditer(r"(?ms)^## (\d+\.\d+)\. [^\n]+\n(.*?)(?=^## |\Z)", text):
        found[match[1]] = match[2].strip()
    return intro, found


def p13_lessons(chapter: str) -> tuple[str, dict[str, str]]:
    text = (ROOT / "authoring" / "P13" / chapter / "manuscript.md").read_text(encoding="utf-8")
    first = re.search(r"(?m)^## P13\.C\d{2}\.L\d{2} — ", text)
    if first is None:
        raise ValueError(f"No P13 lesson: {chapter}")
    intro = text[:first.start()].split("\n", 1)[-1].strip()
    found = {}
    for match in re.finditer(r"(?ms)^## (P13\.C\d{2}\.L\d{2}) — [^\n]+\n(.*?)(?=^## P13\.C|\Z)", text):
        found[match[1]] = match[2].strip()
    return intro, found


def answer_blocks() -> dict[str, str]:
    text = (ROOT / "answers.md").read_text(encoding="utf-8")
    found = {}
    for match in re.finditer(r"(?ms)^(C\d+\.\d+)\. (.*?)(?=^C\d+\.\d+\. |^## |\Z)", text):
        found[match[1]] = match[2].strip()
    return found


def migrate() -> dict:
    tree = json.loads((ARCH / "knowledge_tree.json").read_text(encoding="utf-8"))
    migration = rows("legacy_migration.csv")
    units = rows("legacy_content_units.csv")
    evidence = rows("evidence_ownership.csv")
    lessons = {l["id"]: l for p in tree["parts"] for c in p["chapters"] for l in c["lessons"]}
    bodies: dict[str, list[str]] = defaultdict(list)
    provenance: dict[str, list[str]] = defaultdict(list)
    old_answers = answer_blocks()
    question_text: dict[str, str] = {}
    unit_by_location = {u["old_location"]: u for u in units}
    used_units: set[str] = set()
    used_sections: set[str] = set()
    used_questions: set[str] = set()
    source_paths = sorted((ROOT / "chapters").glob("[0-9][0-9]-*.md"))
    if len(source_paths) != 19:
        raise ValueError(f"Expected 19 legacy chapters, found {len(source_paths)}")
    section_map: dict[str, str] = {}
    for path in source_paths:
        intro, chapter_sections = sections(path)
        relative = f"chapters/{path.name}"
        first_owner = None
        for row in migration:
            if not row["old_location"].startswith(relative + "#") or row["action"] == "move_rekey_after_review":
                continue
            section = row["old_location"].split("#", 1)[1]
            if section not in chapter_sections or section in section_map:
                raise ValueError(f"Section missing or duplicated: {row['old_location']}")
            section_map[section] = relative
            used_sections.add(row["old_location"])
            first_owner = first_owner or row["primary_text_owner"]
            body = chapter_sections[section]
            if row["action"] == "split":
                for ordinal, paragraph in enumerate(re.split(r"\n\s*\n", body), 1):
                    loc = f"{relative}#{section}:paragraph-{ordinal}"
                    unit = unit_by_location.get(loc)
                    if unit is None:
                        raise ValueError(f"Unmapped content: {loc}")
                    digest = hashlib.sha256((f"{relative}#{section}\0{ordinal}\0" + paragraph).encode("utf-8")).hexdigest()
                    if digest != unit["content_sha256"]:
                        raise ValueError(f"Changed content unit: {loc}")
                    owner = unit["primary_lesson_id"]
                    bodies[owner].append(paragraph)
                    provenance[owner].append(unit["old_id"])
                    used_units.add(loc)
                    # Mixed paragraphs retain full context. Extracted claims are
                    # separately indexed in the ledger for editorial rewriting.
            else:
                owner = row["primary_text_owner"]
                bodies[owner].append(body)
                provenance[owner].append(row["old_location"])
        if first_owner is None:
            raise ValueError(f"No migration owner for {path}")
        bodies[first_owner].insert(0, intro)
        provenance[first_owner].insert(0, relative + "#intro")
        for match in re.finditer(r"(?m)^(C\d+\.\d+)\. (.+)$", path.read_text(encoding="utf-8")):
            if match[1] in question_text:
                raise ValueError(f"Duplicate question {match[1]}")
            question_text[match[1]] = match[2]

    qa_by_owner: dict[str, list[dict]] = defaultdict(list)
    evidence_by_owner: dict[str, list[dict]] = defaultdict(list)
    for row in evidence:
        owner = row["primary_lesson_id"]
        if owner not in lessons:
            raise ValueError(f"Unknown evidence owner {owner}")
        evidence_by_owner[owner].append(row)
        if row["kind"] != "exercise_answer":
            continue
        qid = row["old_id"]
        if qid not in question_text or qid not in old_answers or qid in used_questions:
            raise ValueError(f"Broken question-answer pair: {qid}")
        publication_id = f"{owner}.Q{len(qa_by_owner[owner]) + 1:02d}"
        qa_by_owner[owner].append({"id": qid, "publication_id": publication_id,
                                   "question": question_text[qid], "answer": old_answers[qid]})
        used_questions.add(qid)

    p13_question_count = 0
    for chapter_index in range(1, 5):
        ch = f"C{chapter_index:02d}"
        intro, content = p13_lessons(ch)
        for lesson_index in range(1, 4):
            lid = f"P13.{ch}.L{lesson_index:02d}"
            if lid not in content:
                raise ValueError(f"P13 lesson missing: {lid}")
            body = content[lid]
            if lesson_index == 1:
                body = intro + "\n\n" + body
            if lesson_index == 3:
                body = f"{{{{figure:P13.{ch}}}}}\n\n" + body
            bodies[lid].append(body)
            provenance[lid].append(f"authoring/P13/{ch}/manuscript.md#{lid}")
        answer_text = (ROOT / "authoring" / "P13" / ch / "answers.md").read_text(encoding="utf-8")
        for match in re.finditer(r"(?ms)^\*\*(C13\.\d+)\.\*\* (.*?)(?=^\*\*C13\.\d+\.\*\* |\Z)", answer_text):
            qid = match[1]
            found = re.search(rf"(?ms)^### Bài tập {re.escape(qid)}\s*\n(.*?)(?=^### Bài tập |\Z)", content[f"P13.{ch}.L03"])
            if found is None:
                raise ValueError(f"P13 answer without question: {qid}")
            qa_by_owner[f"P13.{ch}.L03"].append({"id": qid, "publication_id": qid,
                                                   "question": found[1].strip(), "answer": match[2].strip()})
            p13_question_count += 1

    if (len(used_sections), len(used_units), len(used_questions), p13_question_count) != (88, 216, 79, 12):
        raise ValueError(f"Migration incomplete: {len(used_sections)}, {len(used_units)}, {len(used_questions)}, {p13_question_count}")
    if used_units != set(unit_by_location):
        raise ValueError("Content unit ledger contains unused rows")
    if set(question_text) != used_questions or set(old_answers) != used_questions:
        raise ValueError("Question or answer missing from evidence ledger")

    # A split paragraph can contain claims for several future lessons. Keep
    # the paragraph intact for its narrative owner, and carry the exact source
    # sentence to each claim owner. This is flagged for later editorial review.
    for row in evidence:
        if row["kind"] != "claim":
            continue
        owner, anchor = row["primary_lesson_id"], row["old_anchor_or_title"]
        if any(anchor in block for block in bodies[owner]):
            continue
        location = row["old_location"]
        source, section = location.split("#")
        source_text = sections(ROOT / source)[1][section]
        position = source_text.find(anchor)
        if position < 0:
            raise ValueError(f"Claim missing at original location: {row['old_id']}")
        start = max(source_text.rfind(". ", 0, position), source_text.rfind("? ", 0, position),
                    source_text.rfind("! ", 0, position), source_text.rfind("\n", 0, position))
        start = start + (2 if source_text[start:start + 2] in (". ", "? ", "! ") else 1)
        ends = [x for x in (source_text.find(". ", position + len(anchor)),
                            source_text.find("? ", position + len(anchor)),
                            source_text.find("! ", position + len(anchor)),
                            source_text.find("\n", position + len(anchor))) if x >= 0]
        end = min(ends) + 1 if ends else len(source_text)
        excerpt = source_text[start:end].strip()
        if anchor not in excerpt:
            raise ValueError(f"Could not extract claim: {row['old_id']}")
        bodies[owner].append(excerpt)
        provenance[owner].append(f"{location}:claim:{row['old_id']}")

    prior_path = OUT / "manifest.json"
    prior = json.loads(prior_path.read_text(encoding="utf-8")) if prior_path.exists() else None
    manifest = {"schema_version": 1, "architecture": "architecture/knowledge_tree.json",
                "phase": "wave_1_migration_candidate", "lessons": {}}
    for lid, lesson in lessons.items():
        p, c, l = lid.split(".")
        path = OUT / p / c / f"{l}.md"
        body = "\n\n".join(bodies[lid]).strip()
        old = prior["lessons"].get(lid) if prior else None
        editorial_override = bool(old and old.get("editorial_override"))
        if editorial_override:
            if not path.is_file():
                raise ValueError(f"Edited lesson missing: {path}")
            body = path.read_text(encoding="utf-8").strip()
            if hashlib.sha256(body.encode("utf-8")).hexdigest() != old["sha256"]:
                raise ValueError(f"Edited lesson changed without review: {path}")
        if body:
            if path.exists() and path.read_text(encoding="utf-8").strip() != body:
                old_digest = hashlib.sha256(path.read_text(encoding="utf-8").strip().encode("utf-8")).hexdigest()
                if not old or old["sha256"] != old_digest:
                    raise ValueError(f"Refusing to overwrite edited lesson: {path}")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(body + "\n", encoding="utf-8")
        elif path.exists():
            raise ValueError(f"Unmapped existing lesson: {path}")
        status = ("pending_authorship" if not body else
                  "migration_fragment" if len(body.split()) < 100 or p == "P14" else "migrated_draft")
        manifest["lessons"][lid] = {
            "parent": lesson["parent"],
            "prerequisites": lesson["prerequisites"],
            "status": status,
            "verification": ("editorial_synthesis_pending_source_review" if editorial_override else
                             "reviewed_baseline_migration" if body else "not_reviewed"),
            "editorial_override": editorial_override,
            "content": str(path.relative_to(ROOT)).replace("\\", "/") if body else None,
            "sha256": hashlib.sha256(body.encode("utf-8")).hexdigest() if body else None,
            "legacy_units": provenance[lid],
            "claim_ids": [e["old_id"] for e in evidence_by_owner[lid] if e["kind"] == "claim"],
            "examples": [e["old_id"] for e in evidence_by_owner[lid] if e["kind"] == "example"],
            "source_ids": sorted({sid for e in evidence_by_owner[lid] if e["kind"] == "claim"
                                  for sid in e["original_source_ids"].split(";") if sid}),
            "qa": qa_by_owner[lid],
        }
    manifest_path = OUT / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


if __name__ == "__main__":
    result = migrate()
    print("MIGRATION_OK", sum(x["content"] is not None for x in result["lessons"].values()), "/178 lessons")
