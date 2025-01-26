import subprocess

subprocess.call("sudo ifconfig wlan0 down" , shell=True)

subprocess.call("sudo macchanger -p wlan0" , shell=True)

subprocess.call("sudo ifconfig wlan0 up" , shell=True)

print("Your MAC address is reset successfully !")