#!/bin/bash

CURRENT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
ROOT_DIR="$(dirname "$CURRENT_DIR")"
export PYTHONPATH="$ROOT_DIR"
SC_DIR="~/Applications/SuperCollider.app/Contents/MacOS/"

echo "########################################"
echo "Running Politics 1 - Digital Discourse"
echo "########################################"
echo ""
echo "Starting virtual environment..."
source "$ROOT_DIR/venv/bin/activate"
echo "Virtual environment successfully booted"

"$ROOT_DIR/venv/bin/python" "$ROOT_DIR/Message_Endpoints/a1_discourse_flask_twilio_twitter_client.py"