#!/bin/sh
set -e

# if models are not present, continue (workflow can put them into ./models before build)
if [ ! -d "$MODEL_DIR" ]; then
  mkdir -p "$MODEL_DIR"
fi

# run app with gunicorn (adjust module name if run:app vs wsgi)
exec gunicorn --bind :8080 --workers 2 run:app
