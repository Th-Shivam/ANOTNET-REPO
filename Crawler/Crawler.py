import requests as rq 

def request(url):
    try: 
        return rq.get("https://" + url)
    except rq.exceptions.ConnectionError:
        pass     

with open("Crawler/files-and-dirs-wordlist.txt" , "r" ) as wordlist:
    for line in wordlist:
        subdomain = line.strip()
        url = "google.com" 
        test_url = f"{url}/{subdomain}" 
        response = request(test_url)
        if response:
            print(f"[+] Discovered url --->  {test_url}")
        else:
            pass         