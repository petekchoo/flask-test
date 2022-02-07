from flask import Flask, render_template, request
application = Flask(__name__)

@application.route('/')
def welcome():
    return render_template('index.html')

@application.route('/form')
def form():
    return render_template('/form.html')
 
@application.route('/data/', methods = ['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form
        return render_template('/data.html',form_data = form_data) 

application.run()