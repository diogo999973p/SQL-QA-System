#!/bin/bash

# Run the script
echo "Executing driver sh"
/usr/local/bin/driver.sh

# Start Flask
echo "Starting flask app"
exec flask run --host=0.0.0.0