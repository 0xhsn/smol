export TYPE=volume
export VOLUME=${1:-volume1/}
export MASTER=${2:-localhost:9000}

uwsgi --http :${PORT:-9001} --wsgi-file src/server.py --master --processes 4 --threads 2 --callable volume
