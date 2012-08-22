#!/usr/bin/env python

import argparse
import json
import os
import urllib
import urlparse

parser = argparse.ArgumentParser()
parser.add_argument('--access_token', required=True)
parser.add_argument('--limit', type=int, default=50)
parser.add_argument('--owner_cursor')
parser.add_argument('--directory', required=True)

args = parser.parse_args()

q = []
q.append('SELECT object_id, src_big, owner_cursor FROM photo')
q.append('WHERE owner=me()')
if args.owner_cursor:
  q.append('AND owner_cursor < "%s"' % (args.owner_cursor))
q.append('LIMIT %i' % (args.limit))

url = 'https://graph.facebook.com/fql'

params = urllib.urlencode({
  'access_token': args.access_token,
  'q': ' '.join(q),
})

data = json.loads(urllib.urlopen('%s?%s' % (url, params)).read())

for row in data['data']:
  filename = urlparse.urlparse(row['src_big']).path.split('/')[-1]
  path = os.path.abspath('/'.join([args.directory, filename]))
  if os.path.exists(path):
    continue
  blob = urllib.urlopen(row['src_big']).read()
  f = open(path, 'w')
  f.write(blob)
  f.close()
