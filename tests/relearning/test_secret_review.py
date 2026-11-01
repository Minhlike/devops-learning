"""Protect the exact reviewed exceptions and unchanged baseline manifests."""
import json
import subprocess
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
BASE='817ad0da74e5fac644c713f7e591815ac4ce2135'

class SecretReview(unittest.TestCase):
    def test_only_reviewed_exact_historical_exceptions(self):
        findings=json.loads((ROOT/'docs/relearning/qa/gitleaks-findings.json').read_text())
        actual={line for line in (ROOT/'.gitleaksignore').read_text().splitlines()
                if line and not line.startswith('#')}
        additional=json.loads((ROOT/'docs/relearning/qa/additional-gitleaks-findings.json').read_text())
        self.assertEqual(len(findings),12)
        self.assertEqual(len(additional),2)
        self.assertEqual(len(actual),14)
        self.assertEqual(actual,{row['fingerprint'] for row in findings+additional})
        for row in additional:
            self.assertEqual(row['classification'],'false_positive_business_identifier')
            self.assertEqual(row['source_commit'],'53d5d8f2d63bbf1e4de797861c5bea18623020d5')
            self.assertIn(row['line'],[19,36])
            self.assertEqual(row['fingerprint'],f"{row['source_commit']}:{row['referenced_path']}:generic-api-key:{row['line']}")
        for row in findings:
            self.assertEqual(row['classification'],'false_positive_checksum')
            self.assertEqual(row['fingerprint'],f"{BASE}:{row['manifest']}:generic-api-key:{row['line']}")

    def test_all_274_checksums_in_both_manifests_unchanged(self):
        for name in ['LEGACY_BASELINE.json','LEGACY_INITIAL_BASELINE.json']:
            path='state/relearning/'+name
            old=subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
            current=(ROOT/path).read_bytes()
            self.assertEqual(json.loads(old),json.loads(current))
            self.assertEqual(len(json.loads(current)['files']),274)
            self.assertEqual(json.loads(current)['reported_completed'],55)
            self.assertEqual(json.loads(current)['current'],'S56')

    def test_private_keys_are_not_tracked_and_are_ignored(self):
        for path in ['labs/s35-ansible-multihost/s35_key',
                     'tmp/relearning-preservation/labs/s35-ansible-multihost/s35_key']:
            self.assertEqual(subprocess.check_output(['git','ls-files','--',path],cwd=ROOT),b'')
            self.assertEqual(subprocess.run(['git','check-ignore','-q','--',path],cwd=ROOT).returncode,0)

if __name__=='__main__':unittest.main()
