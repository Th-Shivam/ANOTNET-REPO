import requests

def download(url):
    get_request = requests.get(url)
    file_name = url.split("/")[-1]
    with open( file_name , "wb") as output_file :
        output_file.write(get_request.content)

download("test url")    