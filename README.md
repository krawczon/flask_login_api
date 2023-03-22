# flask_login_api
# app.py

Flask web application for user registration and login.

The application uses a database to store user data, and provides basic functionality for creating an account, logging in, and logging out.

The code consists of several routes:

/ - the home page that allows users to log in or go to the registration page.
    If the user is already logged in, they are redirected to their user page.

/registration - the registration page that allows users to create an account.
    If the user is already logged in, they are redirected to their user page.

/user/<username> - the user page that displays the logged-in user's username.
    If the user is not logged in, they are redirected to the home page.

/logout - a route that logs the user out by clearing the logged_in key in the session object and redirecting to the home page.

The application uses the Flask render_template function to render HTML templates,
and the request and session objects to handle user input and store session data.

The database module is used to interact with the database.
The Db class in this module provides methods for inserting and retrieving data from the database.

Overall, this code provides a basic example of user registration and login functionality using Flask and a simple database.
However, it is important to note that this code is not production-ready,
and would need to be further developed and secured before being deployed in a real-world application.
