#!/bin/bash
cd src
python3 -m unittest discover -v -p "test_*.py"
