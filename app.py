import os
from dotenv import load_dotenv
import requests
from flask import Flask, render_template
app = Flask(__name__)

load_dotenv()
url = os.environ.get("URL")
user = os.environ.get("USERNAME")
passwd = os.environ.get("PASS")

@app.route('/')
def index():
    r = requests.get(url, auth=(user, passwd), verify=False)
    devices = r.json()
    return render_template("index.html", devices=devices)
