#! usr/bin/env python

import scapy.all as scapy
import optparse
import pyfiglet
import requests
from tabulate import tabulate
from colorama import init
from termcolor import colored


ascii_banner = pyfiglet.figlet_format("Network Scanner\n By Zeckers")
print(ascii_banner)


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="-t Enter an IP to scan")
    (options, arguments) = parser.parse_args()
    if not options.target:
        parser.error("[-] -t Please specify an IP, use --help for more info")
    return options


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    client_list = []
    for element in answered:
       client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
       client_list.append(client_dict)
       #print(element[1].psrc + "\t\t" + element[1].hwsrc)
    return (client_list)


def print_results(results_list):
    print(colored("\nIP" + "\t\t\t" + "Mac Address" + "\t\t\t" + "MAC Vendor / Hostname", "white", "on_red"))
    print("------------------------------------------------------------------------------")
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"] + "\t\t" + requests.get('http://api.macvendors.com/' + client["mac"]).text)


options = get_arguments()
scan_results = scan(options.target)
print_results(scan_results)

