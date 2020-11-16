#!/bin/bash

while 'true'
do
  echo "Running App..."
  gunicorn cloudy.app:APP --workers 1 --threads 8 --bind 0.0.0.0:8080
  echo "App exited. Trying again soon."
  sleep 10
done
