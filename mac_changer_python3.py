import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="interface to change MAC")
    parser.add_option("-m", "--mac", dest="new_mac", help="new_mac address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[+] Specify an interface, More info --help")
    elif not options.new_mac:
        parser.error("[+] Specify a new_mac, for more use --help")
    return options


def change_mac(interface, new_mac):
    print(" [+] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    ifconfig_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    if ifconfig_search_result:
        return ifconfig_search_result.group(0)
    else:
        print("[+] Couldn't read MAC address")


options = get_arguments()

current_mac = get_current_mac(options.interface)
print("Current MAC > " + str(current_mac))

change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] MAC address successfully changed to " + current_mac)
else:
    print("[-] MAC address didn't get changed")

