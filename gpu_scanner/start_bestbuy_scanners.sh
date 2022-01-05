#!/bin/bash

# all tasks are killed with a single ctrl+c
(trap 'kill 0' INT; 
    python3 bestbuy_scanner.py 6439402 & 
    python3 bestbuy_scanner.py 6429442 & 
    python3 bestbuy_scanner.py 6429434 &
    python3 bestbuy_scanner.py 6429440 &
    python3 bestbuy_scanner.py 6428324 &
    python3 bestbuy_scanner.py 6426149 &
    python3 bestbuy_scanner.py 6471615
)