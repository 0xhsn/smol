import os
from rocksdb_python import Options, PyDB, ReadOptions
import json
import socket
import hashlib
import random

options = Options()
options.IncreaseParallelism()

print('sup', os.environ['TYPE'])

def resp(start_response, code, headers=[('Content-type', 'text/plain')], body=b''):
  start_response(code, headers)
  return [body]

# *** Master Server ***
if os.environ['TYPE'] == 'master':
  volumes = os.environ['VOLUMES'].split(',')

  for v in volumes:
    print(v)

  db = PyDB(options, "./olivedb")

def master(env, start_response):
  key = env['REQUEST_URI']
  metakey = db.Get(ReadOptions(), key.encode('utf-8'))

  if metakey is None:
    if env['REQUEST_METHOD'] == 'PUT':
        # TODO: make it smarter
        volume = random.choice(volumes)
        
        # Save volume to database
        meta = {"volume": volume}
        db.put(key.encode('utf-8'), json.dumps(meta).encode('utf-8'))
    else:
      resp(start_response, '404 Not Found', body=b'key not found')
  else:
      meta = json.loads(metakey.decode('utf-8'))

  # send redirect to volume server for GET + PUT + DELETE
  print(meta)
  volume = meta['volume']
  headers = [('Location', 'http://%s%s' % (volume, key))]
  return resp(start_response, '307 Temporary Redirect', headers=headers)

# *** Volume Server ***

class FileCache(object):
  def __init__(self, basedir):
    self.basedir = os.path.realpath(basedir)
    os.makedirs(self.basedir, exist_ok=True)
    print("FileCache in %s" % basedir)

  def k2p(self, key, mkdir_ok=False):
    # Must be MD5 hash
    assert len(key) == 32

    path = self.basedir+"/"+key[0:2]+"/"+key[0:4]
    if not os.path.isdir(path) and mkdir_ok:
      os.makedirs(path, exist_ok=True)

    return os.path.join(path, key)

  def exists(self, key):
    return os.path.isfile(self.k2p(key))

  def delete(self, key):
    os.unlink(self.k2p(key))

  def get(self, key):
    return open(self.k2p(key), "rb").read()

  def put(self, key, value):
    with open(self.k2p(key, True), "wb") as f:
      f.write(value)

if os.environ['TYPE'] == "volume":
  host = socket.gethostname()
  fc = FileCache(os.environ['VOLUME'])

def volume(env, start_response):
  key = env['REQUEST_URI'].encode('utf-8')
  hkey = hashlib.md5(key).hexdigest()
  print(hkey)

  if env['REQUEST_METHOD'] == 'PUT':
    flen = int(env.get('CONTENT_LENGTH', '0'))
    if flen > 0:
        data = env['wsgi.input'].read(flen)
        fc.put(hkey, data)
        return resp(start_response, '201 Created', body=b'')
    else:
        return resp(start_response, '411 Length Required', body=b'content length required')
  
  if not fc.exists(hkey):
    return resp(start_response, '404 Not Found', body=b'key not found')
  
  if env['REQUEST_METHOD'] == 'GET':
    return resp(start_response, '200 OK', body=fc.get(hkey))

  if env['REQUEST_METHOD'] == 'DELETE':
    fc.delete(hkey)
    return resp(start_response, '200 OK', body=b'') 
