import argparse
import glob
import os.path
import json
from utils import *

parser = argparse.ArgumentParser()
parser.add_argument('inpath')
parser.add_argument('outpath')
parser.add_argument('--all', action='store_true')
args = parser.parse_args()

dfiles = glob.glob(os.path.join(args.inpath, 'd-*'))
sfiles = glob.glob(os.path.join(args.inpath, 's-*'))

days = {}
for df in dfiles:
    if df[-19:-9] not in days:
        days[df[-19:-9]] = []
    days[df[-19:-9]] += [df]
for sf in sfiles:
    days[sf[-19:-9]] += [sf]

for day in days:
    days[day].sort(key=lambda x: (os.path.basename(x)[1:] +
                                  os.path.basename(x)[0]))

for day in days:
    if args.all is False and day != sorted(days.keys())[-1]:
        print('skipping', day)
        continue
    path = os.path.join(args.outpath, day + '.json')
    day_data = {}

    print('gen-data | ', day, '-->', path)

    with open(path, 'w+') as fh:
        d = s = df = sf = None
        for f in days[day]:
            if os.path.basename(f)[0] == 'd' and int(f[-5:-3]) % 5 == 0:
                try:
                    df = f
                    with open(f) as dfh:
                        d = json.load(dfh)
                except json.decoder.JSONDecodeError as e:
                    d = None
            if os.path.basename(f)[0] == 's' and int(f[-5:-3]) % 5 == 0:
                try:
                    sf = f
                    with open(f) as sfh:
                        s = json.load(sfh)
                except json.decoder.JSONDecodeError as e:
                    s = None
            if d is not None and s is not None and df[-5:] == sf[-5:]:
                timestamp = f[-19:]
                timestamp_data = {'c': d['cashBalance'], 's': []}
                for stock in d['assets']:
                    try:
                        price = get_price(s['results'], stock['symbol'])
                    except Exception as e:
                        print(df, sf, e, f, timestamp, stock['symbol'])
                        price = None
                    timestamp_data['s'] += [{
                        't': stock['symbol'],
                        'n': stock['shares'],
                        'c': round(stock['avgCost'], 3),
                        'p': (round(float(price), 3)
                              if price is not None
                              else None)
                    }]
                day_data[timestamp] = timestamp_data
                d = s = None
        json.dump(day_data, fh, separators=(',', ':'))

print('gen-data | done')
