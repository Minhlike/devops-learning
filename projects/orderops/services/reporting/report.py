"""Read an authorized snapshot; never connect with application write credentials."""
import csv
from decimal import Decimal, InvalidOperation

def summarize(source):
    count=0
    total=Decimal('0')
    seen=set()
    for row in csv.DictReader(source):
        if row['order_id'] in seen: raise ValueError('duplicate order_id')
        seen.add(row['order_id'])
        value=Decimal(row['total'])
        if not value.is_finite() or value<0: raise ValueError('invalid total')
        count+=1; total+=value
    return {'orders':count,'total':str(total)}

if __name__=='__main__':
    import argparse,json
    parser=argparse.ArgumentParser(); parser.add_argument('snapshot')
    args=parser.parse_args()
    try:
        with open(args.snapshot,encoding='utf-8',newline='') as source:
            print(json.dumps(summarize(source)))
    except (OSError,ValueError,KeyError,InvalidOperation) as error:
        parser.exit(1,f'report failed: {type(error).__name__}\n')
