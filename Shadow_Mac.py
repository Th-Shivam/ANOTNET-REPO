import subprocess
import optparse

parser  = optparse.OptionParser() 

parser.add_option("-i" , "--interface" dest="innterface" ,  help = "Use this to set the interface")

parser.parse_args()

interface = input("Enter the interface name for which you want to change the MAC :")

new_mac = input("Enter the new MAC address :")

subprocess.call("sudo ifconfig " + interface + "down" , shell=True)

subprocess.call("sudo ifconfig " + interface + "hw ether"+ new_mac , shell=True)

subprocess.call("sudo ifconfig " + interface + "up" , shell=True)

print("Your mac is changed succesfully !")

