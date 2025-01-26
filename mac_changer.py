import subprocess

subprocess.call("sudo ifconfig wlan0 down" , shell=True)

subprocess.call("sudo ifconfig wlan0 hw ether 00:11:22:33:44:55" , shell=True)

subprocess.call("sudo ifconfig wlan0 up" , shell=True)

print("Your mac is changed succesfully !")

