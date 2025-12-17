import requests
import re

def get_links(target_url):        
    response = requests.get(target_url)
    return re.findall('(?:href=")(.*?)"' , response.text )
         
url = "https://zsecurity.org" 
href_links = get_links(url)
for link in href_links:
    if url in link:
        print(link)

