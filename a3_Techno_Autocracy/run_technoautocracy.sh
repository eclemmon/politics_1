#!/bin/bash

CURRENT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
ROOT_DIR="$(dirname "$CURRENT_DIR")"
export PYTHONPATH="$ROOT_DIR"
SC_DIR="/Applications/SuperCollider.app/Contents/MacOS"
SC_SCRIPT_PATH="$ROOT_DIR/a3_Techno_Autocracy/sc_files/technoautocracy_main.scd"

echo "########################################"
echo "Running Politics 1 - Technoautocracy"
echo "########################################"
echo ""
echo "Starting virtual environment..."
source "$ROOT_DIR/venv/bin/activate"
echo "Virtual environment successfully booted"

"$ROOT_DIR/venv/bin/python" "$ROOT_DIR/Message_Endpoints/a3_technoautocracy_flask_twilio_twitter_client.py" &
"$SC_DIR/sclang" "$SC_SCRIPT_PATH" &
processing-java --sketch="$ROOT_DIR/a3_Techno_Autocracy/visualization_files/a3_technoautocracy/" --run &
echo "For technoautocracy you have to run the script from technoautocracy_run.scd for now!"