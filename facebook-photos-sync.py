#!/usr/bin/env python

import argparse
import json
import os
import urllib
import urlparse

parser = argparse.ArgumentParser()
parser.add_argument('--access_token', required=True)
parser.add_argument('--limit', type=int, default=50)
parser.add_argument('--owner_cursor_file')
parser.add_argument('--directory', required=True)

args = parser.parse_args()

q = []
q.append('SELECT images, owner_cursor FROM photo WHERE owner=me()')
if args.owner_cursor_file and os.path.exists(args.owner_cursor_file):
  f = open(args.owner_cursor_file, 'r')
  q.append('AND owner_cursor < "%s"' % (f.read()))
  f.close()
q.append('LIMIT %i' % (args.limit))

url = 'https://graph.facebook.com/fql'

params = urllib.urlencode({
  'access_token': args.access_token,
  'q': ' '.join(q),
})

data = json.loads(urllib.urlopen('%s?%s' % (url, params)).read())

if args.owner_cursor_file and len(data['data']):
  f = open(args.owner_cursor_file, 'w')
  f.write(data['data'][0]['owner_cursor'])
  f.close()

for row in data['data']:
  images = row['images']
  images.sort(key=lambda value: value['width'])
  source = images[-1]['source']
  filename = urlparse.urlparse(source).path.split('/')[-1]
  path = os.path.abspath('/'.join([args.directory, filename]))
  if os.path.exists(path):
    continue
  blob = urllib.urlopen(source).read()
  f = open(path, 'w')
  f.write(blob)
  f.close()
