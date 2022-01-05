#!/bin/bash

# all tasks are killed with a single ctrl+c
(trap 'kill 0' INT; 
    python3 evga_scanner.py 10G-P5-3897-RX & 
    python3 evga_scanner.py 08G-P5-3667-RX & 
    python3 evga_scanner.py 10G-P5-3885-RX 
)


# python3 evga_scanner.py 08G-P5-3665-RX &
# python3 evga_scanner.py 08G-P5-3663-RX &
# python3 evga_scanner.py 10G-P5-3895-RX &
# python3 evga_scanner.py 10G-P5-3883-RX &
# python3 evga_scanner.py 10G-P5-3881-RX