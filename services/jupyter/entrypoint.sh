#!/bin/bash

# Run the script
/usr/local/bin/driver.sh

# Start Jupyter Notebook
exec jupyter notebook --ip=0.0.0.0 --port=8000 --no-browser --allow-root