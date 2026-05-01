import os
from dotenv import load_dotenv
import requests
from flask import Flask, render_template
from turbo_flask import Turbo
import threading
import time
from mac_vendor_lookup import MacLookup

mac = MacLookup()
mac.update_vendors()


load_dotenv()
url = os.environ.get("URL")
user = os.environ.get("USERNAME")
passwd = os.environ.get("PASS")

# app = Flask(__name__)


# @app.route('/')
# def index():
#     r = requests.get(url, auth=(user, passwd), verify=False)
#     devices = r.json()
#     for device in devices:
#         if device['status'] == 'bound':
#             try:
#                 device['vendor'] = mac.lookup(device["active-mac-address"])
#             except:
#                 #print(device['active-mac-address'])
#                 device['vendor'] = 'NaN😜'
#     return render_template("index.html", devices=devices)


app = Flask(__name__)
turbo = Turbo(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.context_processor
def inject_data():
    # r = requests.get("https://timeapi.io/api/v1/time/current/unix")
    # data = r.json()
    # return {'data': data}
    r = requests.get(url, auth=(user, passwd), verify=False)
    devices = r.json()
    for device in devices:
        if device['status'] == 'bound':
            try:
                device['vendor'] = mac.lookup(device["active-mac-address"])
            except:
                device['vendor'] = 'NaN😜'
            # if device['hostname'] == None:
                # device['hostname'] = '-'
    return {'devices': devices}


def update_data():
    with app.app_context():
        while True:
            time.sleep(5)
            turbo.push(turbo.replace(render_template('index.html'), 'devices'))

@app.before_request
def before_first_request():
    threading.Thread(target=update_data).start()