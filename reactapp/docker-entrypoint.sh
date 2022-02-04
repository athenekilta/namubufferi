#!/bin/sh
set -eu
mkdir -p node_modules
if [ -z "$(ls -A node_modules)" ]; then
  set -x
  yarn install
fi
set -x
exec "$@"
