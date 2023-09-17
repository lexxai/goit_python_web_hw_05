#!/bin/bash

# turn on bash's job control
set -m

# Start the process and put it in the background
python hw_05/server_websoket.py &

python hw_05/server_http_async.py
