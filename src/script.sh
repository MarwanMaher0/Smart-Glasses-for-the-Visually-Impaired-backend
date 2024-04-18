#!/bin/bash

# Change to the directory where Basics.py is located
cd ~/Desktop/alpha/VALL-E-X

# Receive input from stdin (response_text)
input=$(cat)

# Save input to a temporary text file
echo "$input" > temp_input.txt

# Execute Basics.py to generate audio based on the input
python3 Basics.py < temp_input.txt
