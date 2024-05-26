import os
from rocksdb_python import Options, PyDB, ReadOptions, WriteOptions
options = Options()
options.IncreaseParallelism()

print('sup', os.environ['TYPE'])

if os.environ['TYPE'] == 'master':
  db = PyDB(options, "./olivedb")
  print(db.Get(ReadOptions(), b"k1"))

def master(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return [b"sup master"]

def volume(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return [b"sup volume"]
