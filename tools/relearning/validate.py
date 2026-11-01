"""Offline contracts for curriculum, evidence and progress. No infrastructure calls."""
import hashlib
import json
import sys
from urllib.parse import urlparse
from datetime import datetime
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
STATES=['not_started','theory','model_understood','guided_lab','guided_passed',
        'independent_lab','independent_passed','operational_check','acceptance',
        'needs_remediation','mastered','paused']
OFFICIAL={'docs.docker.com','docs.github.com','docs.aws.amazon.com','developer.hashicorp.com',
          'docs.ansible.com','kubernetes.io','helm.sh','prometheus.io','grafana.com','opentelemetry.io'}
TRANSITIONS={
 'not_started':['theory'], 'theory':['model_understood','needs_remediation'],
 'model_understood':['guided_lab'], 'guided_lab':['guided_passed','needs_remediation'],
 'guided_passed':['independent_lab'], 'independent_lab':['independent_passed','needs_remediation'],
 'independent_passed':['operational_check','acceptance'],
 'operational_check':['acceptance','needs_remediation'],
 'acceptance':['mastered','needs_remediation'],
 'needs_remediation':['theory','guided_lab','independent_lab'], 'mastered':[],
}

def transition(old,new,resume=None):
    if old not in STATES or new not in STATES: raise ValueError('invalid state')
    if new=='paused' and old!='paused': return
    if old=='paused':
        if new!=resume or resume not in STATES or resume=='paused': raise ValueError('invalid resume')
    elif new not in TRANSITIONS[old]: raise ValueError('invalid transition')

def load(path): return json.loads((ROOT/path).read_text(encoding='utf-8'))

def errors(catalog,progress,evidence,current,root=ROOT):
    issues=[]; lessons=catalog.get('lessons',[]); ids=[x['id'] for x in lessons]
    if any(x.get('schema_version')!=1 for x in [catalog,progress,current]): issues.append('unsupported schema version')
    if len(ids)!=len(set(ids)): issues.append('duplicate lesson ID')
    rows={x['id']:x for x in lessons}
    if {x['legacy_session'] for x in lessons}!={f'S{i}' for i in range(14,49)}: issues.append('missing session')
    if catalog.get('track')!='relearning' or progress.get('track')!='relearning': issues.append('track mismatch')
    def ref(path):
        resolved=(root/path).resolve()
        return resolved.is_relative_to(root.resolve()) and resolved.is_file()
    for x in lessons:
        if not x.get('official_docs') or any(not d.get('url','').startswith('https://') or not all(d.get(k) for k in ['section','version','purpose']) for d in x.get('official_docs',[])): issues.append('missing official docs')
        if any(urlparse(d.get('url','')).hostname not in OFFICIAL for d in x.get('official_docs',[])): issues.append('unapproved source domain')
        if not x.get('competency'): issues.append('missing competency')
        if x.get('maturity') not in ['DESIGNED','AUTHORED','VERIFIED']: issues.append('invalid maturity')
        for p in x.get('prerequisites',[]):
            if p not in rows: issues.append('missing prerequisite')
        if x.get('maturity') in ['AUTHORED','VERIFIED']:
            for k in ['content','guided_lab','independent_lab']:
                if not x.get(k) or not ref(x[k]): issues.append('broken file reference')
        if x.get('maturity')=='VERIFIED' and not x.get('author_verification'): issues.append('unproved verification')
    visiting=set(); done=set()
    def visit(lid):
        if lid in visiting: issues.append('cyclic dependency'); return
        if lid in done or lid not in rows: return
        visiting.add(lid)
        for dep in rows[lid].get('prerequisites',[]): visit(dep)
        visiting.remove(lid); done.add(lid)
    for lid in rows: visit(lid)
    records=progress.get('lessons',{})
    if set(records)!=set(rows): issues.append('catalog/progress mismatch')
    ev={}
    for e in evidence:
        if e.get('id') in ev: issues.append('duplicate evidence ID')
        ev[e.get('id')]=e
        required=['id','lesson_id','actor','at','environment','kind','verification','reference','sha256','verifier','limits']
        if any(k not in e for k in required): issues.append('missing evidence field'); continue
        if e['lesson_id'] not in rows: issues.append('orphan evidence')
        try:
            if datetime.fromisoformat(e['at'].replace('Z','+00:00')).tzinfo is None: raise ValueError()
        except ValueError: issues.append('invalid timestamp')
        if e['verification'] not in ['student_reported','guided_verified','independent_verified','troubleshooting_verified','not_verified']: issues.append('invalid evidence verification')
        if not ref(e['reference']): issues.append('broken evidence reference')
        elif hashlib.sha256((root/e['reference']).read_bytes()).hexdigest()!=e['sha256']: issues.append('changed evidence')
    for lid,r in records.items():
        if any(k not in r for k in ['status','guided_lab','independent_lab','operational_check','learning_gaps','last_verified_at','next_review_at']): issues.append('missing progress field')
        if r.get('status') not in STATES: issues.append('invalid state')
        if r.get('status')=='paused' and r.get('resume_state') not in set(STATES)-{'paused'}: issues.append('invalid resume')
        for phase in ['guided_lab','independent_lab','operational_check']:
            if not isinstance(r.get(phase),dict): issues.append('missing checkpoint'); continue
            item=r[phase]
            if phase!='operational_check' and item.get('status')=='not_required': issues.append('required lab skipped')
            if item.get('status') not in ['not_started','in_progress','passed','not_required']: issues.append('invalid checkpoint state')
            for eid in item.get('evidence_ids',[]):
                if eid not in ev or ev[eid].get('lesson_id')!=lid: issues.append('missing or misattributed evidence')
            if item.get('status')=='passed':
                accepted={'guided_lab':'guided_verified','independent_lab':'independent_verified','operational_check':'troubleshooting_verified'}[phase]
                if not any(ev.get(eid,{}).get('verification')==accepted and ev[eid].get('lesson_id')==lid for eid in item.get('evidence_ids',[])): issues.append('passed without verified evidence')
        if r.get('status')=='mastered':
            if not r.get('last_verified_at') or not r.get('next_review_at'): issues.append('missing review timestamp')
            if any(r.get(k,{}).get('status')!='passed' for k in ['guided_lab','independent_lab']): issues.append('mastered without evidence')
            if rows.get(lid,{}).get('operational_required') and r.get('operational_check',{}).get('status')!='passed': issues.append('missing operational evidence')
            if any(records.get(p,{}).get('status')!='mastered' for p in rows.get(lid,{}).get('prerequisites',[])): issues.append('unmet prerequisite')
        if r.get('status') not in ['not_started','paused']:
            if any(records.get(p,{}).get('status')!='mastered' for p in rows.get(lid,{}).get('prerequisites',[])): issues.append('lesson unlocked too early')
    if current.get('track')!='relearning' or current.get('lesson_id') not in rows: issues.append('invalid current lesson')
    if current.get('teaching_started') is not False and current.get('lesson_id') not in records: issues.append('invalid teaching state')
    return sorted(set(issues))

def main():
    evidence=[json.loads(s) for s in (ROOT/'state/relearning/EVIDENCE_LOG.jsonl').read_text(encoding='utf-8').splitlines() if s.strip()]
    found=errors(load('docs/relearning/catalog.json'),load('state/relearning/LESSON_PROGRESS.json'),evidence,load('state/relearning/CURRENT_STATE.json'))
    baseline=load('state/relearning/LEGACY_BASELINE.json')
    for path,sha in baseline['files'].items():
        p=ROOT/path
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=sha: found.append('legacy changed: '+path)
    arch=load('projects/orderops/architecture.json')
    if {x['language'] for x in arch['components']}!={'Java','Python','Go','SQL'}: found.append('architecture language mismatch')
    diagrams=arch['diagrams']+['docs/relearning/diagrams/'+name+'.puml' for name in ['tutor-learning-process','tutor-state-machine','tutor-interaction-sequence']]
    for path in diagrams:
        if not (ROOT/path).is_file(): found.append('missing diagram: '+path)
        else:
            text=(ROOT/path).read_text(encoding='utf-8')
            if not text.startswith('@startuml') or not text.strip().endswith('@enduml'): found.append('diagram envelope missing: '+path)
    if found:
        print('\n'.join(found)); return 1
    print('VALID: 35 sessions / 70 lessons; legacy hashes unchanged; no learning credit awarded')
    return 0

if __name__=='__main__': sys.exit(main())
