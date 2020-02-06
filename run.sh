#!/bin/bash

# from https://stackoverflow.com/a/22644006/149987
trap "exit" INT TERM
trap "kill 0" EXIT

# grabbed this badboy from https://stackoverflow.com/a/246128/149987
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

while true
do
  bspc subscribe node_focus | $DIR/golden.py
done
