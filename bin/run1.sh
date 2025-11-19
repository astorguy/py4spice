#!/bin/bash

SCRIPT_PATH="/workspaces/py4spice/circuits/sec_1_04_01_dividers/python"
SCRIPT_NAME="sec_1_04_01.py"

# Construct the full command
COMMAND="uv run \"${SCRIPT_PATH}/${SCRIPT_NAME}\""

# 1. Print the command to the terminal
echo "${COMMAND}"

# 2. Execute the command
eval "${COMMAND}"
