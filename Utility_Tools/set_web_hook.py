from datetime import datetime
from pyngrok import ngrok, conf, installer
from twilio.rest import Client
from dotenv import load_dotenv
import ssl
import os

def run_ngrok_set_webhook():
    """
    Automator function for setting the ngrok and twilio webhooks
    :return: ngrok process
    """
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
    pyngrok_config = conf.get_default()

    if not os.path.exists(pyngrok_config.ngrok_path):
        myssl = ssl.create_default_context();
        myssl.check_hostname = False
        myssl.verify_mode = ssl.CERT_NONE
        installer.install_ngrok(pyngrok_config.ngrok_path, context=myssl)

    ngrok_process = run_ngrok_set_webhook()
    try:
        # Block until CTRL-C or some other terminating event
        ngrok_process.proc.wait()
    except KeyboardInterrupt:
        print(" Shutting down server.")
        ngrok.kill()

