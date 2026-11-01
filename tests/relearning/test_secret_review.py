"""Protect the exact reviewed exceptions and unchanged baseline manifests."""
import json
import subprocess
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
BASE='817ad0da74e5fac644c713f7e591815ac4ce2135'

class SecretReview(unittest.TestCase):
    def test_only_twelve_exact_historical_exceptions(self):
        findings=json.loads((ROOT/'docs/relearning/qa/gitleaks-findings.json').read_text())
        actual={line for line in (ROOT/'.gitleaksignore').read_text().splitlines()
                if line and not line.startswith('#')}
        self.assertEqual(len(actual),12)
        self.assertEqual(actual,{row['fingerprint'] for row in findings})
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
