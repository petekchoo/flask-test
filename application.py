from flask import Flask, render_template, request, redirect, url_for
application = Flask(__name__)

@application.route('/', methods = ['POST', 'GET'])
def welcome():
    return render_template('index.html', variableA = 0, variableB = 1)

@application.route('/form')
def form():
    return render_template('/form.html')
 
@application.route('/data', methods = ['POST', 'GET'])
def data():
    if request.method == 'GET':
        return "The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        dataForm = request.form
        return render_template('/data.html', form_data = dataForm)

def manipulateInputs(inputA, inputB):
    strTempA = inputA
    strTempB = inputB

    return strTempB, strTempA