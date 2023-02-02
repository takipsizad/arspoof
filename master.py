import base64
import flask
from flask import request
import scapy
import requests
from scapy.layers import http
from itsdangerous import base64_decode
import arpspoof
from cryptography.fernet import Fernet
app = flask.Flask(__name__)
key = base64.b64encode(b"plshelpplshelpplshelpplshelppppp")

f = Fernet(key)
@app.route("/slol")
def lol():
    ccallback = request.args.get('d')
    pkt = f.decrypt(ccallback)
    print(base64.b64_decode(pkt))

app.run(port=9615,host="0.0.0.0")