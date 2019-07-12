#!/bin/bash

# grabbed this badboy from https://stackoverflow.com/a/246128/149987
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

while true
do
  bspc subscribe node_focus | $DIR/golden.py
done
