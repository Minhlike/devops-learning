import copy
import json
import unittest
from pathlib import Path
from tools.relearning.validate import ROOT, errors, load, transition, TRANSITIONS

class Contracts(unittest.TestCase):
    def setUp(self):
        self.c=load('docs/relearning/catalog.json')
        self.p=load('state/relearning/LESSON_PROGRESS.json')
        self.s=load('state/relearning/CURRENT_STATE.json')
        self.first=self.c['lessons'][0]['id']
    def check(self): return errors(self.c,self.p,[],self.s)
    def test_baseline(self): self.assertEqual(self.check(),[])
    def test_duplicate(self):
        self.c['lessons'].append(copy.deepcopy(self.c['lessons'][0]))
        self.assertIn('duplicate lesson ID',self.check())
    def test_missing_prerequisite(self):
        self.c['lessons'][0]['prerequisites']=['missing']
        self.assertIn('missing prerequisite',self.check())
    def test_cycle(self):
        self.c['lessons'][0]['prerequisites']=[self.c['lessons'][-1]['id']]
        self.assertIn('cyclic dependency',self.check())
    def test_mastered_without_evidence(self):
        self.p['lessons'][self.first]['status']='mastered'
        self.assertIn('mastered without evidence',self.check())
    def test_missing_docs(self):
        self.c['lessons'][0]['official_docs']=[]
        self.assertIn('missing official docs',self.check())
    def test_invalid_state(self):
        self.p['lessons'][self.first]['status']='completed'
        self.assertIn('invalid state',self.check())
    def test_broken_file(self):
        self.c['lessons'][0]['content']='missing.md'
        self.assertIn('broken file reference',self.check())
    def test_evidence_owner_and_verification(self):
        self.p['lessons'][self.first]['guided_lab']={'status':'passed','evidence_ids':['e1']}
        self.assertIn('missing or misattributed evidence',self.check())
        self.assertIn('passed without verified evidence',self.check())
    def test_catalog_mismatch_and_schema(self):
        self.p['lessons'].pop(self.first);self.p['schema_version']=2
        self.assertIn('catalog/progress mismatch',self.check())
        self.assertIn('unsupported schema version',self.check())
    def test_prerequisite_gate(self):
        self.p['lessons'][self.c['lessons'][1]['id']]['status']='theory'
        self.assertIn('lesson unlocked too early',self.check())
    def test_pause_and_illegal_shortcuts(self):
        transition('guided_lab','paused');transition('paused','guided_lab','guided_lab')
        with self.assertRaises(ValueError): transition('paused','mastered','guided_lab')
        with self.assertRaises(ValueError): transition('not_started','mastered')
    def test_uml_edges_match_code(self):
        uml=(ROOT/'docs/relearning/diagrams/tutor-state-machine.puml').read_text(encoding='utf-8')
        for a,bs in TRANSITIONS.items():
            for b in bs: self.assertIn(a+' --> '+b,uml)

if __name__=='__main__':unittest.main()
