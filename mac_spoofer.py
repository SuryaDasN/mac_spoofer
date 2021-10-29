#!/usr/bin/env python3

import subprocess
import argparse
import re
import time


def get_argument():
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--interface", dest="interface", help="interface to change its MAC address")
	parser.add_argument("-m", "--mac", dest="new_mac", help="New MAC address")
	options = parser.parse_args()
	if not options.interface:
		parser.error("[-] Please specify an interface, use --help for more info.")
	elif not options.new_mac:
		parser.error("[-] Please specify a new MAC address, use --help for more info.")
	return options

def change_mac(interface, new_mac):
	subprocess.call(["ifconfig", interface, "down"])
	subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
	subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
	ifconfig_result = subprocess.check_output(["ifconfig", interface]).decode('utf-8')
	mac_addresss_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

	if mac_addresss_search_result:
		return (mac_addresss_search_result.group(0))	
	else:
		print("[-] Could not read MAC address.")
		exit()


if __name__ == '__main__':

	options = get_argument()

	try:
		original_mac = get_current_mac(options.interface)
		print(f"[-] Current MAC : {original_mac}")

		change_mac(options.interface, options.new_mac)
		print(f"[+] Changing MAC address of {options.interface} to {options.new_mac}")
		
		current_mac = get_current_mac(options.interface)
		
		if current_mac == options.new_mac:
			print(f"[+] MAC address successfully changed to {options.new_mac}")
			print("[=] Press CRTL + C to revert back.")
		else:
			print("[-] MAC address did not get changed ")

		time_elapsed = 0
		while(True):
			print(f"\r[+] Time elapsed : {time_elapsed}", end="")
			time_elapsed += 2
			time.sleep(2)

	except KeyboardInterrupt:
		print("\n[-] Detected CRTL + C ")
		print("[+] Reverting MAC address... Please wait...")
		change_mac(options.interface, original_mac)
