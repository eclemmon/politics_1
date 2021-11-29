#!/bin/bash

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
SC_DIR="~/Applications/SuperCollider.app/Contents/MacOS/"
SECRET_KEY="abc123"

echo "##################"
echo "Running Politics 1"
echo "##################"

source "$SCRIPT_DIR/venv/bin/activate"

command() {
  sleep 3
  python3.8 "$SCRIPT_DIR/Message_Endpoints/flask_twilio_twitter_client.py"
}

redis-server & python3.8 "$SCRIPT_DIR/flask_twilio_twitter_server.py" & command

trap "{ echo 'SHUTTING DOWN'; redis-cli shutdown; kill $(pgrep -f flask); }" INT
