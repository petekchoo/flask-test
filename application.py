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
    fileFiveLetters = open("data/fiveletterwords.txt", "r")
     
    if request.method == 'POST':
        
        for i in range(1, 6):
            if request.form.get('l'+str(i)+'g') == None:
                greenlist.append(None)

            else:
                greenlist.append(request.form.get('l'+str(i)+'g'))

        for letter in request.form.get('grey'):
            greylist.append(letter)

        for i in range(1, 6):
            for letter in request.form.get('l'+str(i)+'y'):
                yellowlist[i-1].append(letter)

        strgrey = ''.join(greylist)

        bestword = runChecks(fileFiveLetters, greylist, yellowlist, greenlist)

        return render_template(
            'form.html', 
            green = greenlist, 
            grey = greylist, 
            yellow = yellowlist, 
            word = bestword,
            l1g = request.form.get('l1g'),
            l2g = request.form.get('l2g'),
            l3g = request.form.get('l3g'),
            l4g = request.form.get('l4g'),
            l5g = request.form.get('l5g'),
            l1y = ''.join(request.form.get('l1y')),
            l2y = request.form.get('l2y'),
            l3y = request.form.get('l3y'),
            l4y = request.form.get('l4y'),
            l5y = request.form.get('l5y'),
            strgrey = strgrey
        )

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

# creates list of words that don't contain any of the letters in lstCant
def cantList(wordlist, cant):

    lstWords = []
    boolMatch = True
    
    for word in wordlist:

        for letter in cant:
            if letter in word:
                boolMatch = False
        
        if boolMatch == True:
            lstWords.append(word.strip())
        
        else:
            boolMatch = True
    
    return lstWords

# creates list of words that don't contain any of the letters in lstDont in a specific position
def dontList(wordlist, dont):

    lstWords = []
    intPosition = 0
    boolMatch = True

    for word in wordlist:

        for item in dont:

            for letter in item:

                if word.strip()[intPosition] == letter:
                    boolMatch = False
        
            intPosition += 1

        if boolMatch == True: #bool([x for x in item if(x in word)]) == True:
            intPosition = 0
            lstWords.append(word.strip())
        
        else:
            boolMatch = True
            intPosition = 0

    return lstWords

# creates a list of words that contains the set of letters, but not in the designated positions
def includeList(wordlist, dont):

    lstWords = []
    lstDont = list({x for l in dont for x in l})
    boolMatch = True
    
    if lstDont == []:
        return wordlist

    for word in wordlist:
        for letter in lstDont:
            if letter not in word:
                boolMatch = False
    
        if boolMatch == True:
            lstWords.append(word.strip())
        
        else:
            boolMatch = True
    
    return lstWords


# creates list of words that contain exact letters in lstMust by position (greenlist)
def mustList(wordlist, must):

    lstWords = []
    intPosition = 0
    boolMatch = True

    for word in wordlist:

        for item in must:

            if word.strip()[intPosition] == item or item == "":
                intPosition += 1
            
            else:
                boolMatch = False
        
        if boolMatch == True:
            intPosition = 0
            lstWords.append(word.strip())
        
        else:
            boolMatch = True
            intPosition = 0
    
    return lstWords

def topWord(wordlist):

    intWords = len(wordlist)
    lstCount = [0 for x in range(26)]
    numNewScore = 1
    numBestScore = 0
    strMaxWord = ""

    for word in wordlist:
        for letter in list(set(word)):
            lstCount[ord(letter) - 97] = lstCount[ord(letter) - 97] + 1

    lstCoef = [x/intWords for x in lstCount]
    
    for word in wordlist:
        
        if len(word) == len(list(set(word))):
            for letter in word:
                numNewScore = numNewScore * lstCoef[ord(letter) - 97]

        else:
            for letter in list(set(word)):
                numNewScore = numNewScore * lstCoef[ord(letter) - 97] * 1/(len(word) - len(list(set(wordlist))) - len(wordlist))
        # print(word, numNewScore)
        
        if numNewScore > numBestScore:
            numBestScore = numNewScore
            numNewScore = 1
            strMaxWord = word
        
        else:
            numNewScore = 1
    
    return strMaxWord

def runChecks(wordlist, cant, dont, must):

    list1 = cantList(wordlist, cant)
    list2 = dontList(list1, dont)
    list3 = includeList(list2, dont)
    list4 = mustList(list3, must)

    return topWord(list4)