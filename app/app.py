from flask import Flask, render_template,request,redirect,url_for,session
import json
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
@app.route("/")
def main():
    return render_template('main.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Then get the data from the form
        username = request.form['username']
        password = request.form['password']
        # Get the user associated with these credentials
        
        with open ('db.json') as f:
            data = json.load(f)
            print(data['users'])
            for user in data['users']:
                print(user)
                if username == user['username'] and password == user['password']:
                    session['user'] = user
                    return redirect(url_for('profile'))
                    
            else:
                return render_template('login.html', error="Invalid username or password")
        
        # Or you could have a custom template for displaying the info
        # return render_template('asset_information.html',
        #                        username=user, 
        #                        password=password)

    # Otherwise this was a normal GET request
    else:   
        return render_template('login.html',error = '')
@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/signup")
def signup():
    return render_template('signupquiz.html')

@app.route("/matches")
def match():
    currentuser = session['user']
    session['matches'] = []
    elo=0
    with open ('db.json') as f:
            data = json.load(f)
            for user in data['users']:
                if user != currentuser:
                    if any(item in user['interests'] for item in currentuser['skills']) and any(item in currentuser['interests'] for item in user['skills']):
                        
                        for item in user['skills']:
                            if item in currentuser['interests']:
                                elo += 100
                            else:
                                elo += 0
                        session['matches'].append([user,elo])

    session['matches'].sort(key=lambda x: x[1],reverse=True)
    matches = [match[0] for match in session['matches']]
    return render_template('matchpage.html',matches=matches)
    

@app.route("/profile")
def profile():
    print('GOT USER')
    user = session['user']
    print(user['name'])
    return render_template('profile.html',user=user)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080,debug=True)