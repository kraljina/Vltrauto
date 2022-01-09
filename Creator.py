import json
from pprint import pprint
import random
#from random import randint
from time import sleep
import string

from vultr import Vultr, VultrError


def load_config():
    try:
        with open("config.json") as json_file:
            return json.load(json_file)
    except:
        print("config.json not found ! ")
        exit(0)


CONFIG = load_config()

with open(CONFIG["INSTANCE_Config"].get("Stack_script"), "r") as f:
    stack = f.read()

user_ssh_key = open(CONFIG.get("RSA_public_Path")).read()


def get_region(vultr):
    conf = CONFIG["INSTANCE_Config"].get("region")
    if str(conf).lower() == "random":
        regions = list(vultr.regions.list().keys())
        return regions[random.randint(0, len(regions) - 1)]
    else:
        return conf


def create(vultr, osid, vpsplanid, stackid, sshid):
    cid = int(get_region(vultr))
    print(f"[+] Creating With Region ID : {cid} ", end=" ")
    N = 7    
    server_name = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = N))
    print(f"\nCreating With Server Name : {server_name}")
    return vultr.server.create(
        dcid=cid,
        vpsplanid=vpsplanid,
        osid=osid,
        params={
            "SCRIPTID": stackid,
            "SSHKEYID": sshid,
            "label":server_name
        },
    )


def main(count):
    for token in CONFIG.get("Tokens"):
        vultr = Vultr(token)

        print(f"[+] Woking On account : {vultr.account.info()}")

        sshid = vultr.sshkey.create(name="SSHKEY", ssh_key=user_ssh_key).get(
            "SSHKEYID", None
        )
        if not sshid:
            exit()
        print(f"[+] SSH Key Created : {sshid}")

        stackid = vultr.startupscript.create(name="STACK", script=stack).get(
            "SCRIPTID", None
        )
        if not sshid:
            exit()
        print(f"[+] Stack Script Created : {stackid}")

        osid = int(CONFIG["INSTANCE_Config"].get("OSID"))
        vpsplanid = int(CONFIG["INSTANCE_Config"].get("VPSPLANID"))

        print(f"[+] OS ID : {osid} | Plan ID : {vpsplanid} ")
        try:
            for i in range(count):
                instance = create(vultr, osid, vpsplanid, stackid, sshid)
                print(instance)
        except VultrError as e:
            print(f"\n[!] Error : {e}")
            continue


if __name__ == '__main__':
    main(CONFIG.get("INSTANCE_PER_TOKEN"))
    for token in CONFIG.get("Tokens"):
        vultr = Vultr(token)
        print("*" * 80)
        print("[+] Waiting  Creation ...")
        sleep(10)
        for server, value in vultr.server.list().items():
            print("Server ", server, end=" ")
            print(" IP : ", value["main_ip"])
            with open(CONFIG.get("SAVE_IP_TO_FILE"), "a") as f:
                f.write(value["main_ip"] + "\n")
