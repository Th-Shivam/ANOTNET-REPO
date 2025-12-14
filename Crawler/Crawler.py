import requests as rq 

def request(url):
    try: 
        return rq.get("https://" + url)
    except rq.exceptions.ConnectionError:
        pass     

with open("subdomains-wordlist.txt" , "r" ) as wordlist:
    for line in wordlist:
        subdomain = line.strip()
        url = "google.com" 
        test_url = f"{subdomain}.{url}" 
        response = request(test_url)
        if response:
            print(f"[+] Discovered subdomain --->  {test_url}")
        else:
            pass         