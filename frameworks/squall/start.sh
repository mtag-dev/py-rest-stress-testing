#!/bin/bash

until $(python -c "import squall" 2> /dev/null); do
    echo Wait for squall install
    sleep 1
done

/usr/local/bin/gunicorn -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8080 app:app
