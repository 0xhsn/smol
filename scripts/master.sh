export TYPE=master
export DB=../olivedb

uwsgi --http :${PORT:-9000}  --wsgi-file src/server.py --master --processes 4 --threads 2 --callable master
