from datetime import datetime
from pyngrok import ngrok
from twilio.rest import Client
from dotenv import load_dotenv


def run_ngrok_set_webhook():
    load_dotenv()
    # get datetime
    now = datetime.now()
    subdomain = "politics-1-" + now.strftime("%m%d%Y")
    ng = ngrok.connect(8000, subdomain=subdomain)
    url = ng.public_url
    print(url)
    client = Client()
    client.incoming_phone_numbers.list(phone_number="+19293343697")[0].update(sms_url=url + "/sms")
    return ngrok.get_ngrok_process()


if __name__ == "__main__":
    ngrok_process = run_ngrok_set_webhook()
    try:
        # Block until CTRL-C or some other terminating event
        ngrok_process.proc.wait()
    except KeyboardInterrupt:
        print(" Shutting down server.")
        ngrok.kill()

