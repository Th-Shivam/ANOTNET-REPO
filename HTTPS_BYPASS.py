#1 . Run the arp spoofer script and make sure the target is the victim and the router is the gateway.
#2 . Run the sslstrip script to strip the https from the target.
#3 . Run the iptables command to redirect the traffic to the queue .
#4 . Generally the sslstrip is working on port 10000 , so we need to redirect the traffic to the queue on port 10000.
#5 . use this comamand to redirect the traffic to the queue on port 10000.
#6 . iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000 
#7 . Now we can run anything that we want to and it will simply be working like any http site . 