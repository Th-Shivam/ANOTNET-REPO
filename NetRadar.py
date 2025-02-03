import scapy.all as scapy
import argparse 

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") 
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1 , verbose = False)[0]
    
    client_list = []
    for element in answered_list:
        client_dict = {"ip":element[1].psrc, "mac":element[1].hwsrc}
        client_list.append(client_dict)       
    return client_list

def print_result(result_list):
    print("\n[-]Net Radar is active ")
    print("\nNET RADAR IS SCANNING THE NETWORK \n" )
    print("\nNET RADAR CAUGHT THE FOLLOWING IP AND MAC ADDRESS \n")     
    print("IP\t\t\tMAC Address\n----------------------------------------------------------")
    for client in result_list:
        print(client["ip"] + "\t\t" + client["mac"])

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Target IP / IP range.")
    options = parser.parse_args()
    return options

options = get_arguments()
scan_results = scan(options.target) 
print_result(scan_results)

#THIS SCRIPT IS WRITTEN BY SHVAM SINGH @CEO & FOUNDER ANOTNET . 
