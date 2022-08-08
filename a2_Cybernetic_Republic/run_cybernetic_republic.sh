#!/bin/bash

trap "pkill -P $$" SIGINT EXIT

CURRENT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
ROOT_DIR="$(dirname "$CURRENT_DIR")"
export PYTHONPATH="$ROOT_DIR"
SC_DIR="/Applications/SuperCollider.app/Contents/MacOS"
SC_SCRIPT_PATH="$ROOT_DIR/a2_Cybernetic_republic/sc_files/cybernetic_republic_main.scd"

kill $(pgrep -f sclang)

echo "########################################"
echo "Running Politics 1 - Cybernetic Republic"
echo "########################################"
echo ""
echo "Starting virtual environment..."
source "$ROOT_DIR/venv/bin/activate"
echo "Virtual environment successfully booted"

processing-java --sketch="$ROOT_DIR/a2_Cybernetic_Republic/visualization_files/a2_cybernetic_republic/" --run &
"$SC_DIR/sclang" "$SC_SCRIPT_PATH" &
sleep 45
"$ROOT_DIR/venv/bin/python" "$ROOT_DIR/Message_Endpoints/a2_cybernetic_republic_flask_twilio_twitter_client.py"

