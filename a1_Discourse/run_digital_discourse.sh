#!/bin/bash

CURRENT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
ROOT_DIR="$(dirname "$CURRENT_DIR")"
export PYTHONPATH="$ROOT_DIR"
set -a; source "$ROOT_DIR/.env"; set +a;

if [ $DAW = "true" ]
then
  SC_SCRIPT_PATH="$ROOT_DIR/a1_Discourse/sc_files/daw_base/discourse_main.scd"
else
  SC_SCRIPT_PATH="$ROOT_DIR/a1_Discourse/sc_files/sc_base/discourse_main.scd"
fi

echo "########################################"
echo "Running Politics 1 - Digital Discourse"
echo "########################################"
echo ""
echo "Starting virtual environment..."
source "$ROOT_DIR/venv/bin/activate"
echo "Virtual environment successfully booted"
"$ROOT_DIR/venv/bin/python" "$ROOT_DIR/Message_Endpoints/a1_discourse_flask_twilio_twitter_client.py" &
"$SC_DIR/sclang" "$SC_SCRIPT_PATH"