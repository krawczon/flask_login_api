from flask import Flask, render_template, request, redirect, url_for, session
import database

app = Flask(__name__)
app.secret_key = "secretkey"

db = database.Db()

@app.route('/', methods=['GET', 'POST'])
def home():
    error = None
    username = None
    session['logged_in'] = None
    if request.method == 'POST':
        email    = request.form['email']
        password = request.form['password']

        db_email = db.get('email', 'email', email)
        db_password = db.get('password','password', password)
        username = db.get('username', 'email', email)

        if email != db_email or password != db_password:
            error = 'Wrong email address or password. Try arain!'
        else:
            session['logged_in'] = True
            return redirect(url_for('user', username=username))
        
    return render_template('home.html', error=error)

@app.route('/reqistration', methods=['GET', 'POST'])
def registration():
    error= None
    if request.method == 'POST':
        username    = request.form['username']
        email       = request.form['email']
        password    = request.form['password']
        re_password = request.form['re-password']
        
        user_data = (username, email, password)

        if email == db.get('email', 'email', email):
            error = 'This email adress already exists.'
        elif password != re_password:
            error = 'Password is not the same. Try again.'
        else:
            msg='Account is created and ready to use. You can log in now.'
            db.insert(user_data)
            return redirect(url_for('home'))
            
    return render_template('registration.html', error=error)

@app.route('/user/<username>')
def user(username):
    if not session['logged_in']:
        return redirect(url_for('home'))
    else:
        return render_template('user.html', username = username)

@app.route('/logout')
def logout():
    session['logged_in'] = None
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run()
