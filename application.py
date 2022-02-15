from flask import Flask, render_template, request, redirect, url_for
application = Flask(__name__)

@application.route('/')
def homepage():
    return render_template('index.html')

# allow both GET and POST requests
@application.route('/form-example', methods=['GET', 'POST'])
def form_example():
    # handle the POST request
    greenlist = []
    greylist = []
    yellowlist = [[], [], [], [], []]
    bestword = ""
     
    if request.method == 'POST':
        
        for i in range(1, 6):
            greenlist.append(request.form.get('l'+str(i)+'g'))

        for letter in request.form.get('grey'):
            greylist.append(letter)

        for i in range(1, 6):
            for letter in request.form.get('l'+str(i)+'y'):
                yellowlist[i-1].append(letter)

        return render_template('form.html', green = greenlist, grey = greylist, yellow = yellowlist, word = bestword)

    # otherwise handle the GET request
    return '''
           <form method="POST">
    <div><label>Letter 1 Green: <input type="text" name="l1g"></label></div>
    <div><label>Letter 2 Green: <input type="text" name="l2g"></label></div>
    <div><label>Letter 3 Green: <input type="text" name="l3g"></label></div>
    <div><label>Letter 4 Green: <input type="text" name="l4g"></label></div>
    <div><label>Letter 5 Green: <input type="text" name="l5g"></label></div>
    <div><label>Letter 1 Yellows: <input type="text" name="l1y"></label></div>
    <div><label>Letter 2 Yellows: <input type="text" name="l2y"></label></div>
    <div><label>Letter 3 Yellows: <input type="text" name="l3y"></label></div>
    <div><label>Letter 4 Yellows: <input type="text" name="l4y"></label></div>
    <div><label>Letter 5 Yellows: <input type="text" name="l5y"></label></div>
    <div><label>Grey Letters: <input type="text" name="grey"></label></div>
    <input type="submit" value="Submit"></form>'''