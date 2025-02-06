import subprocess
import re
import optparse

def  parse():
    parser  = optparse.OptionParser() 
    parser.add_option("-i" , "--interface" , dest="interface" ,  help = "Use this to set the interface")
    parser.add_option("-m" , "--mac" , dest="new_mac" ,  help = "Use this to set the interface")
    (options , arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface to chane the mac for ")
    if not options.new_mac:
         parser.error("[-] Please specify a new mac to chane  ")   
    return options 

def change_mac(interface , new_mac):
    subprocess.call(f"sudo ifconfig {interface} down", shell=True)
    subprocess.call(f"sudo ifconfig {interface} hw ether {new_mac}", shell=True)
    subprocess.call(f"sudo ifconfig {interface} up", shell=True)
    print("Your mac is changed succesfully !")

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig" , interface]).decode('utf-8')
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w" , ifconfig_result)
    if mac_address_search_result:  
       return mac_address_search_result.group(0)
    else:   
        print("[-] Could not read mac address")    
     
options = parse()
current_mac  = get_current_mac(options.interface)
print(f"Current mac is : {current_mac}")
change_mac(options.interface , options.new_mac) 

current_mac  = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print(f"Mac address was succesfully changed to {current_mac}")
else:
    print("Mac address did not get changed")


# Run the script with sudo permission in linux 

# The script is written by SHIVAM SINGH 
