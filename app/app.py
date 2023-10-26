from flask import Flask, render_template,request

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
        

        return 'The credentials were %s and %s' % (username, password) 
        # Or you could have a custom template for displaying the info
        # return render_template('asset_information.html',
        #                        username=user, 
        #                        password=password)

    # Otherwise this was a normal GET request
    else:   
        return render_template('login.html')
@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/signup")
def signup():
    return render_template('signupquiz.html')

@app.route("/match")
def match():
    return render_template('match.html')



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080,debug=True)