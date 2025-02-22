import scapy.all as scapy

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=2, verbose=False)[0]

    if answered_list:
        return answered_list[0][1].hwsrc
    return None  

def process_sniffed_packet(packet):
    try:
        if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
            real_mac = get_mac(packet[scapy.ARP].psrc)
            response_mac = packet[scapy.ARP].hwsrc

            if real_mac is None:
                print("[!] Unable to get real MAC address. Check network connectivity.")
                return

            if real_mac != response_mac:
                print("[ALERT] Possible ARP Spoofing Detected!")
            else:
                print("[+] You are safe")
    except IndexError:
        pass  

def sniff(interface):        
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)

sniff("wlan0")  
