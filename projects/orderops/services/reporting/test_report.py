import io,unittest
from report import summarize
class ReportTests(unittest.TestCase):
    def test_exact_decimal(self):
        self.assertEqual(summarize(io.StringIO('order_id,total\na,0.10\nb,0.20\n')),{'orders':2,'total':'0.30'})
    def test_duplicate(self):
        with self.assertRaises(ValueError): summarize(io.StringIO('order_id,total\na,1\na,1\n'))
    def test_invalid(self):
        for amount in ['-1','NaN','Infinity']:
            with self.assertRaises(ValueError): summarize(io.StringIO('order_id,total\na,'+amount+'\n'))
