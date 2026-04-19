import requests
import os

def download_assignments(base_url, start=0, end=13, save_folder="assignments"):

    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    for i in range(start, end + 1):
        try:
            
            url = base_url.replace("assigment_2", f"assigment_{i}")
            
            print(f"Downloading: {url}")
            
            response = requests.get(url)
            
            if response.status_code == 200:
                file_path = os.path.join(save_folder, f"assignment_{i}.pdf")
                
                with open(file_path, "wb") as f:
                    f.write(response.content)
                
                print(f"✅ Downloaded: assignment_{i}.pdf")
            else:
                print(f"❌ Failed (Status {response.status_code}): assignment_{i}")
        
        except Exception as e:
            print(f"⚠️ Error downloading assignment_{i}: {e}")


base_url = "https://archive.nptel.ac.in/content/storage2/courses/downloads_new/110105142/noc20_mg30_assigment_2.pdf"

download_assignments(base_url)
