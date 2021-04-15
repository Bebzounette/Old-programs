#!usr/bin/env python

import subprocess
import optparse
import random
import re
from tabulate import tabulate
from colorama import init
from termcolor import colored
import pyfiglet


ascii_banner = pyfiglet.figlet_format("MacChanger\n By Zeckers")
print(ascii_banner)

def rand_mac():
    return "02:%02x:%02x:%02x:%02x:%02x" % (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
        )

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its Mac Address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info")
    return options


def Mac_Changer(interface, mac_address):
    print(colored("[+] Changing Mac Address for " + interface + "  to " + results, "yellow"))
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", results])
    subprocess.call(["ifconfig", interface, "up"])

def check(interface):
    ifconfig_results = subprocess.check_output(["ifconfig", options.interface])
    search = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_results)
    if search:
        return search.group(0)
    else:
        print(colored("Sorry, couldn't read the MAC Address", "red"))

results = rand_mac()
options = get_arguments()


current_mac = check(options.interface)
print("Current MAC Address = " + str(current_mac))

Mac_Changer(options.interface, results)

current_mac = check(options.interface)
if current_mac == results:
    print(colored("[+] MAC Address was successfully changed to " + current_mac +"\n\n", "green"))
else:
    print(colored("[-] MAC Address did not changed.\n", "red"))
