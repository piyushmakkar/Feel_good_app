from kivy.app import App
from kivy.lang import Builder
#buider helps to connect kv file with python file
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from hoverable import HoverBehavior
from datetime import datetime
from pathlib import Path
import json
import glob
import random


Builder.load_file('design.kv')

class LoginScreen(Screen):
    
    def sign_up(self):
        
        self.manager.transition.direction = "left"
        self.manager.current = "sign_up_screen"

    def login_done(self,uname,pswd):
        
        with open("users.json") as file:
            users = json.load(file) 

        if uname in users.keys() and users[uname]['password'] == pswd:
            self.manager.current = "login_sucess_screen"
            self.ids.username.text = ""
            self.ids.password.text = ""
        
        elif  self.ids.username.text == "" or self.ids.password.text == "":
            self.ids.wrong_cred.text = "Text field(s) cannot be empty"
        
        else:
            self.ids.username.text = ""
            self.ids.password.text = ""
            self.ids.wrong_cred.text = "Wrong Username or Password"

    def forgot_password(self):

        self.manager.transition.direction = "left"
        self.manager.current = "forgot_password_screen"

    def change_password(self):
        
        self.manager.transition.direction = "left"
        self.manager.current = "change_password_screen"

class RootWidget(ScreenManager):
    
    pass

class SignUpScreen(Screen):
    
    def add_user(self,uname,pswd):
       
        with open("users.json") as file:
            users = json.load(file) 
        
        if uname in users.keys() :
            self.ids.username.text = ""
            self.ids.password.text = ""
            self.ids.user_already_exists.text = "Username Taken"
        
        elif  self.ids.username.text == "" or self.ids.password.text == "":
            self.ids.user_already_exists.text = "Text field(s) cannot be empty"
        
        else:
            users[uname] = {'username':uname,'password':pswd,
            'created':datetime.now().strftime("%Y-%m-%D %H-%M-%S")}
            with open("users.json","w") as file:
                json.dump(users,file) 
            self.manager.current = "sign_up_sucess_screen"

    def go_back(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"        

class SignUpSuccessScreen(Screen):
    
    def login_now(self):
        
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

class LoginSuccessScreen(Screen):
    
    def log_out(self):
       
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"
        self.ids.mood.text = ""

    
    def display_quotes(self,mood):
       
        mood = mood.lower()
        available_moods = glob.glob("q/*txt")
        
        available_moods = [Path(filename).stem for filename in available_moods]
    
        if mood in available_moods:
            with open(f"q/{mood}.txt",encoding="utf8") as file:
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)
       
        else:
            self.ids.mood.text = ""
            self.ids.quote.text = "Please select from Happy, Sad and Unloved"  

class ForgotPasswordScreen(Screen):
    
    def login_page(self):

        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

class ChangePasswordScreen(Screen):
    
    def login_page(self):

        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

class ImageButton(ButtonBehavior,HoverBehavior,Image):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__ == "__main__":
    MainApp().run()