import os
from dotenv import load_dotenv
import requests
from flask import Flask
app = Flask(__name__)

load_dotenv()
url = os.environ.get("URL")
user = os.environ.get("USER")
passwd = os.environ.get("PASS")

print(url)

@app.route('/api/devices')
def get_data():
    r = requests.get(url, auth=(user, passwd), verify=False)
    return r.json()

