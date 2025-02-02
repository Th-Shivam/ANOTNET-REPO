import scapy.all as scapy

def scan(ip):
    arp_request = scapy.arp(psdt=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") 
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadccast , timeout = 1 )[0]
    for element in answered_list:
        print(element[1].psrc)
        print(element[1].hwsrc)
        print("-----------------------------------------------------------------------------")
        print("NET RADAR CAUGHT THE FOLLOWING IP AND MAC ADDRESS")
        

scan("127.0.0.1")    
