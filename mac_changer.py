import subprocess

import optparse

parser  = optparse.OptionParser() 

parser.add_option("-i" , "--interface" , dest="interface" ,  help = "Use this to set the interface")
parser.add_option("-m" , "--mac" , dest="new_mac" ,  help = "Use this to set the interface")

(options,arguments) = parser.parse_args()

interface = options.interface
new_mac = options.new_mac

subprocess.call(f"sudo ifconfig {interface} down", shell=True)
subprocess.call(f"sudo ifconfig {interface} hw ether {new_mac}", shell=True)
subprocess.call(f"sudo ifconfig {interface} up", shell=True)

print("Your mac is changed succesfully !")

