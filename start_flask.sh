#!/bin/bash
touch ~/.Xauthority
xauth add ${HOST}:0 . $(xxd -l 16 -p /dev/urandom)
xauth list
python3 api.py 
