import os
from dotenv import load_dotenv
import requests
from flask import Flask, render_template
from turbo_flask import Turbo
import threading
import time
from mac_vendor_lookup import MacLookup
import urllib3

urllib3.disable_warnings() # disable ssl warnings

mac = MacLookup()
#mac.update_vendors()


load_dotenv()
url = os.environ.get("URL")
user = os.environ.get("API_USER")
passwd = os.environ.get("API_PASS")

app = Flask(__name__)
turbo = Turbo(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.context_processor
def inject_data():
    r = requests.get(url, auth=(user, passwd), verify=False)
    devices = r.json()
    for device in devices:
        if device['status'] == 'bound':
            try:
                device['vendor'] = mac.lookup(device["active-mac-address"])
            except:
                device['vendor'] = 'NaN😜'
    return {'devices': devices}

thread_started = False
@app.before_request
def before_first_request():
    global thread_started
    if not thread_started:
        threading.Thread(target=update_data, daemon=True).start()
        thread_started = True


def update_data():
    with app.app_context():
        while True:
            time.sleep(10)
            # print("replacing")
            turbo.push(turbo.replace(
                render_template('devices.html'), 'devices'))

if __name__ == '__main__':
    app.run(debug=True, port=8001)
