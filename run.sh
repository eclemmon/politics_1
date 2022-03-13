#!/bin/bash

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
SC_DIR="~/Applications/SuperCollider.app/Contents/MacOS/"
SECRET_KEY="abc123"
NGROK_PID=$(pgrep ngrok)

# Kill running ngrok
kill -9 "($NGROK_PID)"

echo "##################"
echo "Running Politics 1"
echo "##################"

echo $SUB_DOMAIN
source "$SCRIPT_DIR/venv/bin/activate"

redis-server &
python3.8 "$SCRIPT_DIR/flask_twilio_twitter_server.py" &
python3.8 "$SCRIPT_DIR/Utility_Tools/set_web_hook.py";


trap "{ echo 'SHUTTING DOWN'; redis-cli shutdown; kill $(pgrep -f flask); kill $(pgrep ngrok)}" INT

exit


