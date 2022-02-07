from flask import Flask
application = Flask(__name__)

@application.route('/')

def hello_world():
    strUserInput = input("Input word!")
    
    return strUserInput