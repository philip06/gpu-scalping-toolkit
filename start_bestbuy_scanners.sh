#!/bin/bash

# all tasks are killed with a single ctrl+c
(trap 'kill 0' INT; 
    python3 -m gpu_scalping_toolkit.gpu_scanner.bestbuy_scanner 6439402 & 
    python3 -m gpu_scalping_toolkit.gpu_scanner.bestbuy_scanner 6429442 & 
    python3 -m gpu_scalping_toolkit.gpu_scanner.bestbuy_scanner 6429434 &
    python3 -m gpu_scalping_toolkit.gpu_scanner.bestbuy_scanner 6429440 &
    python3 -m gpu_scalping_toolkit.gpu_scanner.bestbuy_scanner 6428324 &
    python3 -m gpu_scalping_toolkit.gpu_scanner.bestbuy_scanner 6426149 &
    python3 -m gpu_scalping_toolkit.gpu_scanner.bestbuy_scanner 6471615
)