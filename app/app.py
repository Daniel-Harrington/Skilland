from flask import Flask, render_template,request,redirect,url_for,session
import json
app = Flask(__name__)

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
                    redirect(url_for('match',user=user))
                    return match(user)
                    
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

@app.route("/match")
def match(user):
    print('GOT USER')
    return render_template('matchpage.html')



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080,debug=True)