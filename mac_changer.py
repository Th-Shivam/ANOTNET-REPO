import subprocess

interface = input("Enter the interface name for which you want to change the MAC :")

new_mac = input("Enter the new MAC address :")

subprocess.call("sudo ifconfig " + interface + "down" , shell=True)

subprocess.call("sudo ifconfig " + interface + "hw ether"+ new_mac , shell=True)

subprocess.call("sudo ifconfig " + interface + "up" , shell=True)

print("Your mac is changed succesfully !")

