import sys

from vultr import Vultr, VultrError

api_keys = ["7SLE6OSQZSRS4WEYPG37EMN7AOY3QWPVIYTQ"]

def remove_all(v):
    for i, key in v.server.list().items():
        print("[+] Removing ", i, "...", end=" ")
        try:
            v.server.destroy(subid=i)
        except VultrError:
            print("")
            print(sys.exc_info()[1])
            continue
        print(" Done")


for api_key in api_keys:
    print("[+] Api :", api_key)
    v = Vultr(api_key)
    remove_all(v)
