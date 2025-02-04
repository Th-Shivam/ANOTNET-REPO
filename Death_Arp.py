import scapy.all as scapy
packet = scapy.ARP(op=2, pdst="" , hwdst="" , psrc="")
scapy.send(packet) 