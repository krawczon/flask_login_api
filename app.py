from flask import Flask, render_template, request, redirect, url_for, session
import database

app = Flask(__name__)
app.secret_key = "secretkey"

# Create a database object to interact with the database
db = database.Db()

@app.route('/', methods=['GET', 'POST'])
def home():
    error = None
    username = None

    # Set the logged_in key in the session object to None
    session['logged_in'] = None

    if request.method == 'POST':
        # Get the email and password values from the form
        email    = request.form['email']
        password = request.form['password']

        # Get the email, password, and username values from the database based on the provided email
        db_email = db.get('email', 'email', email)
        db_password = db.get('password','password', password)
        username = db.get('username', 'email', email)

        # If the email or password is incorrect, set an error message
        if email != db_email or password != db_password:
            error = 'Wrong email address or password. Try arain!'
        else:
            # Otherwise, set the logged_in key in the session object to True and redirect to the user page
            session['logged_in'] = True
            return redirect(url_for('user', username=username))
        
    # Render the home page template with the error message, if any
    return render_template('home.html', error=error)


@app.route('/reqistration', methods=['GET', 'POST'])
def registration():
    error= None
    
    if request.method == 'POST':
        # Get the username, email, password, and re-typed password values from the form
        username    = request.form['username']
        email       = request.form['email']
        password    = request.form['password']
        re_password = request.form['re-password']
        
        # Create a tuple with the user data
        user_data = (username, email, password)

        # Check if the provided email already exists in the database
        if email == db.get('email', 'email', email):
            error = 'This email adress already exists.'
        # Check if the provided password and re-typed password match
        elif password != re_password:
            error = 'Password is not the same. Try again.'
        else:
            # If the email and password are valid, insert the user data into the database and redirect to the home page
            msg='Account is created and ready to use. You can log in now.'
            db.insert(user_data)
            return redirect(url_for('home'))
            
    # Render the registration page template with the error message, if any
    return render_template('registration.html', error=error)


@app.route('/user/<username>')
def user(username):
    # If the user is not logged in, redirect to the home page
    if not session['logged_in']:
        return redirect(url_for('home'))
    else:
        # Otherwise, render the user page template with the provided username
        return render_template('user.html', username = username)

@app.route('/logout')
def logout():
    # Set the logged_in key in the session object to None and redirect to the home page
    session['logged_in'] = None
    return redirect(url_for('home'))

if __name__ == '__main__':
    # Run the Flask app
    app.run()
