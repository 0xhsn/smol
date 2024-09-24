# smol
Simple + tiny python-based key-value store.


## Directory Overview
- `olivedb`: where rocksdb (the database used for metadata storage by the master server) stores its data files.
- `volume1`: this is where the volume server stores actual files. two-level directory structure to avoid having too many files in a single directory.
  - 2 char (first layer deep): named based on the first two characters of an MD5 hash.
  - 4 char (two layers deep): named based on the first four characters of the MD5 hash, providing a 
  - Value file(s): file name corresponds to the full MD5 hash of a key. contains the actual data associated with that key. 

## Setup
### rocksdb
`brew install rocksdb`

1.	rocksdb_dump:
This tool is used to dump the contents of a RocksDB database.

```sh
rocksdb_dump --db_path ~/Developer/smol/olivedb --dump_location livedb_dump.txt
```

2.	rocksdb_ldb:
This tool provides an interactive command-line interface to perform various operations on a RocksDB database.

```
rocksdb_ldb
```

- Create a database + first key-value
```sh
# Step 1: Create a subdirectory for the database in the current directory
mkdir -p ./olivedb

# Step 2: Use rocksdb_ldb to create the database and insert a key-value pair with the create_if_missing flag
rocksdb_ldb --db=./olivedb put k1 v1 --create_if_missing

# Step 3: Verify the database creation
rocksdb_ldb --db=./olivedb get k1
```
 
Python Interface on MacOS
```
brew install rocksdb
pip install git+https://github.com/gau-nernst/rocksdb-python.git
```

## Usage

```sh
PORT=<port> ./master
```

```sh
PORT=<port> ./volume
```

### cURL
```sh
curl -X PUT -d bigswag http://localhost:9000/k1 -L -vv
curl -X DELETE http://localhost:9000/k1 -L -vv
curl -L GET http://localhost:9000/k1 -vv
```

## TODO
- [x] Use rocksdb
- [ ] Port to rust?
- [ ] Dockerize
- [ ] Integrate ElasticSearch
  - [ ] Good use case for log aggregation and monitoring?: can be used to store logs from multiple services or applications. Handle large amounts of small files (logs) where they need to be ingested, stored, and queried later.