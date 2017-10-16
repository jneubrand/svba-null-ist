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

data = []

with open(os.path.join(os.path.dirname(__file__), 'digest-static.json')) as f:
    digest_static = json.load(f)
    day = []
    daily_digest = []
    for datapoint in digest_static:
        year, month, nday, hours, mins, secs =\
            (int(datapoint['time'][a:b]) for (a, b) in
             [[0, 4], [5, 7], [8, 10], [11, 13], [14, 16], [17, 19]])
        date = '%02d-%02d-%02d' % (year, month, nday)
        timestamp = '%02d-%02d-%02dT%02d:%02d:00' %\
                    (year, month, nday, hours, mins // 30 * 30)
        if not day or date != day['day']:
            daily_digest = []
            day = {'day': date, 'd': daily_digest}
            data += [day]
            print('digest | Adding day', day['day'], 'as static')
        if mins % 30 < 10:
            if len(day['d']) == 0 or day['d'][-1]['t'] != timestamp:
                # last item in day stale. push an empty one.
                day['d'] += [{'t': timestamp, 'd': {}}]
            if 'cash' in datapoint and 'c' not in day['d'][-1]['d']:
                day['d'][-1]['d']['c'] = round(float(datapoint['cash']), 3)
                if 'h' in day['d'][-1]['d']:
                    # worth came first, now subtract cash from it
                    day['d'][-1]['d']['h'] -= day['d'][-1]['d']['c']
                    day['d'][-1]['d']['h'] = round(day['d'][-1]['d']['h'], 3)
            elif 'worth' in datapoint and 'h' not in day['d'][-1]['d']:
                day['d'][-1]['d']['h'] = round(float(datapoint['worth']), 3)
                if 'c' in day['d'][-1]['d']:
                    # cash came first, now subtract it from worth
                    day['d'][-1]['d']['h'] -= day['d'][-1]['d']['c']
                    day['d'][-1]['d']['h'] = round(day['d'][-1]['d']['h'], 3)

print('gen-digest | finished adding static.')

with open(args.outpath, 'w+') as fh:
    for _day in sorted(days.keys()):
        print('gen-digest | proc day', _day)
        this_year, this_month, this_day =\
            int(_day[0:4]), int(_day[5:7]), int(_day[8:10])
        day = days[_day]
        daily_digest = []
        data += [{'day': _day, 'd': daily_digest}]
        d = s = df = sf = None
        last_timestamp_data = None
        for f in day:
            if os.path.basename(f)[0] == 'd' and int(f[-5:-3]) % 30 == 0:
                try:
                    df = f
                    with open(f) as dfh:
                        d = json.load(dfh)
                except json.decoder.JSONDecodeError as e:
                    d = None
            elif os.path.basename(f)[0] == 's' and int(f[-5:-3]) % 30 == 0:
                try:
                    sf = f
                    with open(f) as sfh:
                        s = json.load(sfh)
                except json.decoder.JSONDecodeError as e:
                    s = None
            # Do we have matching portfolio & market data?
            if d is not None and s is not None and df[-5:] == sf[-5:]:
                timestamp = f[-19:]
                timestamp_data = {'c': round(d['cashBalance'], 3)}
                portfolio_value = 0
                for stock in d['assets']:
                    try:
                        price = get_price(s['results'], stock['symbol'])
                        portfolio_value += float(price) * stock['shares']
                    except Exception as e:
                        pass
                if this_year > 2017 or (this_year == 2017 and this_month >= 8):
                    portfolio_value += sum(
                        0
                        if 'side' in o and o['side'] == 'buy'
                        else o['price'] * o['shares']
                        for o in d['orders'])
                timestamp_data['h'] = round(portfolio_value, 3)
                if not last_timestamp_data or \
                   timestamp_data['c'] != last_timestamp_data['c'] or \
                   timestamp_data['h'] != last_timestamp_data['h']:
                    daily_digest += [{'t': timestamp, 'd': timestamp_data}]
                d = s = None
                last_timestamp_data = timestamp_data
    json.dump(data, fh, separators=(',', ':'))

print('gen-digest | done')
