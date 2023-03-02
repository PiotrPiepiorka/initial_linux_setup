#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Script to perform repetitive tasks automated

Attempt to replace initial bash scripts with more configurable initial setup files.

Usage (as admin):
    $ python initial_linux_setup.py

Created for user with Ubuntu 22.04 LTS

ToDo:
- scripting engine replacing configuration files
- thorough testing
- os.system -> subprocess.run
- remove hardcoding system account

"""

__author__ = "Piotr Piepiórka"
__copyright__ = "Copyright 2023"
__version__ = "0.0.1"

SERVICE_ACCOUNT = "user"
SERVICE_ACCOUNT_PASSWORD = "qwerty"

import os
import subprocess

import click
from colorama import init as colorama_init

colorama_init()


def check_network_connectivity():
    print(f"Network routes:")
    # ip_a = subprocess.run(["ip", "a"], stdout=subprocess.PIPE)
    # ip_a__grep_global = subprocess.run(["grep", "global"], stdin=ip_a.stdout, stdout=subprocess.STDOUT)
    # str(ip_a__grep_global).find("inet")
    os.system("ip routes show")
    if not os.system("ping 8.8.8.8"):
        print(f"Probably no network connectivity!")
        if click.confirm("Do you want to continue?", default=False):
            return True
        else:
            return False

def os_update():
    if check_network_connectivity():
        os.system("apt update")
        os.system("apt full-upgrade -y")



def is_admin():
    if os.geteuid() != 0:
        print(f"Run script with root privileges.\nTrying again with 'sudo'")
        os.system("sudo su")
        result = os.execv(["python3", sys.argv[0], sys.argv])
        exit(result)

def create_service_account(service_acc = SERVICE_ACCOUNT, service_acc_pass = SERVICE_ACCOUNT_PASSWORD):
    # At least check for success...
    os.system(f"useradd -m {service_acc}")
    os.system(f"usermod -a -G sudo {service_acc}")
    cmd = f"bash -c \"echo -e '{service_acc_pass}\\n{service_acc_pass}' | passwd root\""
    subprocess.check_call(cmd, shell=True)
    os.system(f"touch /var/lib/AccountsService/users/{service_acc}")
    f_path = "/var/lib/AccountsService/users/" + service_acc
    with open(f_path, "w") as f:
        f.write("[User]\nSystemAccount=true\n")




def install_packages():
    os.system("xargs -a config/packages.txt apt install")

def call_initial_script():
    return subprocess.call(['sh', './config/initial_script.sh'])

def mirror_file_settings():
    pass

if __name__ == "__main__":
    is_admin()
    create_service_account()
    os_update()
    install_packages()
    mirror_file_settings()
    call_initial_script()
