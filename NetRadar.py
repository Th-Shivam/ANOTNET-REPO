import scapy.all as scapy

def scan(ip):
    scapy.arping(ip)
    

scan("127.0.0.1")    