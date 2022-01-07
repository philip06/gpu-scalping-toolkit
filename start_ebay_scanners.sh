#!/bin/bash

# all tasks are killed with a single ctrl+c
(trap 'kill 0' INT; 
    python3 -m gpu_scalping_toolkit.gpu_scanner.ebay_asus_scanner & 
    python3 -m gpu_scalping_toolkit.gpu_scanner.ebay_asus_scanner
)