import requests
import re

def request(url):
    try:
        return requests.get("https://" + url)
    except requests.exceptions.ConnectionError:
        pass

    
response = request("zsecurity.org")
href_links = re.findall('(?:href=")(.*?)"' , response.text )
print(href_links)     

