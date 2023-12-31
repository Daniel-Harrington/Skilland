from flask import Flask, render_template,request,redirect,url_for,session,jsonify
import json
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'




# function to add to JSON
def add_user(userdata, filename='data.json'):
    with open('app/db.json','r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["users"].append(userdata)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)
 
    # python object to be appended


@app.route("/")
def main():
    with open ('app/db.json') as f:
            data = json.load(f)
            print(data['users'])
            session['maxid'] = max(user['id'] for user in data['users'])

    return render_template('main.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    print(request.method)
    if request.method == 'POST':
        # Then get the data from the form
        username = request.form['username']
        password = request.form['password']
        print(username)
        # Get the user associated with these credentials
        
        with open ('app/db.json') as f:
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


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        session['name'] = request.form['name']
        session['bio'] = request.form['bio']

        return redirect(url_for('quiz1'))
    return render_template('signup.html')

@app.route("/matches")
def match():
    
    currentuser = session['user']
    with open ('app/db.json') as f:
            data = json.load(f)
            if currentuser not in data['users']:
                f.close()
                add_user(currentuser)
    session['matches'] = []
    elo=0
    with open ('app/db.json') as f:
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
    return render_template('match.html',matches=matches,user=currentuser)
    

@app.route("/profile")
def profile():
    print('GOT USER')
    user = session['user']
    print(user['name'])
    return render_template('profile.html',user=user)

@app.route('/quiz1')
def quiz1():
    session['skills'] = {}
    
    return render_template('q_teach1.html')
@app.route('/quiz2')
def quiz2():
    session['interests'] = []
    return render_template('q_learn.html')

@app.route("/div_clicked", methods=['POST'])
def div_clicked():

    data = request.json
    print(data)
    if data and 'div_id' in data:
        print(data['div_id'][:10])
        if data['div_id'][:6] == 'skill_':
            div_id = data['div_id'][6:]
            print(div_id)
            if div_id in session['skills']:
                session['skills'].pop(div_id)
            else:
                session['skills'] = session['skills'] | {div_id:data['selectedValue']}
            
            new_user = {'id':session['maxid']+1,'name':session['name'],'username':session['username'],'password':session['password'],'skills':session['skills']}
            print(new_user)
            session['user'] = new_user

            return jsonify({"result": "success"})
            
        elif data['div_id'][:9] == 'interest_':
            div_id = data['div_id'][9:]
            if div_id in session['interests']:
                session['interests'].pop(div_id)
            else:
                session['interests'].append(div_id)
            
            new_user = {'id':session['maxid']+1,'name':session['name'], 'bio':session['bio'],'username':session['username'],'password':session['password'],'skills':session['skills'],'interests':session['interests']}
            print(new_user)
            session['user'] = new_user

            return jsonify({"result": "success"})
    return jsonify({"result": "failure"})
        
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080,debug=True)