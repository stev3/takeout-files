#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import datetime
import operator
import matplotlib.pyplot as plt


if not os.path.isfile('./searches/all_searches.json'):
  result = []
  for f in os.listdir('./searches'):
    if f.endswith('.json'):
      path = './searches/' + f
      with open(path, "rb") as infile:
          result.append(json.load(infile))

  with open("./searches/all_searches.json", "wb") as outfile:
    json.dump(result, outfile)

total_searches = 0
dates_and_queries = {}
with open('./searches/all_searches.json') as f:
  data = json.load(f)
  for i in data:
    if i.get('event'):
      events = i['event']
      for event in events:
        query = event['query']
        query_text = query['query_text']
        timestamp = query['id'][0]['timestamp_usec']
        timestamp = int(timestamp) / 1000000
        date = datetime.datetime.fromtimestamp(timestamp).strftime('%Y/%m/%d')

        if dates_and_queries.get(date):
          dates_and_queries[date].append(query_text)
        else:
          dates_and_queries[date] = [query_text]

        total_searches += 1

def create_day_window(start, finish):
  date_window = []
  delta = finish - start
  for i in range(delta.days + 1):
    day = start + datetime.timedelta(days=i)
    day = day.strftime('%Y/%m/%d')
    date_window.append(day)
  return date_window

start = min(dates_and_queries, key=str)
finish = max(dates_and_queries, key=str)

start_year, start_month, start_day = start.split('/')
finish_year, finish_month, finish_day = finish.split('/')

start = datetime.date(int(start_year), int(start_month), int(start_day))
finish = datetime.date(int(finish_year), int(finish_month), int(finish_day))

day_window = create_day_window(start,finish)

for day in day_window:
  if not dates_and_queries.get(day):
    dates_and_queries[day] = []

# build list of text queries, sorted by date
sorted_dates_and_queries = sorted(dates_and_queries.items(), key=operator.itemgetter(0))
text_queries = [i[1] for i in sorted_dates_and_queries]
number_of_searches = [len(i) for i in text_queries]

with open('data.csv', 'w') as f:
  f.write('date,searches,queries\n')
  for i in sorted_dates_and_queries:
    date = i[0]
    searches = len(i[1])
    queries = ', '.join(i[1]).encode('utf8')
    f.write('{},{},"{}"\n'.format(date,searches,queries))

  f.close()