#!/bin/bash

set -e

if [ $# -eq 1 ]; then
  sudo docker login --username andrewjw --password $DOCKER_TOKEN
fi

docker build -t andrewjw/directory-size-exporter:latest .
