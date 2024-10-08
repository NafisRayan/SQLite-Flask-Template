from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Database connection
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT UNIQUE NOT NULL,
                   email TEXT UNIQUE NOT NULL,
                   password TEXT NOT NULL)''')
conn.commit()
conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check credentials
        if check_credentials(username, password):
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('profile'))
        else:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username=?", (username,))
            existing_user = cursor.fetchone()
            conn.close()

            if existing_user is None:
                flash('Username does not exist', 'error')
            else:
                flash('Incorrect password', 'error')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            flash('Passwords don\'t match', 'error')
        elif not validate_email(email):
            flash('Invalid email address', 'error')
        else:
            # Check if user already exists
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username=? OR email=?", (username, email))
            existing_user = cursor.fetchone()
            conn.close()

            if existing_user:
                if existing_user[1] == username:
                    flash('User with this username already exists.', 'error')
                else:
                    flash('User with this email address already exists.', 'error')
                print("Flash message set:", session.get('_flashes'))
                return render_template('register.html')  # Re-render the form
            else:
                # Add user to database
                add_user_to_db(username, email, password)
                flash('Registration successful!', 'success')
                print("Flash message set:", session.get('_flashes'))
                return redirect(url_for('login'))

    print("No POST request, rendering register page")
    return render_template('register.html')

@app.route('/profile')
def profile():
    if 'logged_in' in session:
        return render_template('profile.html', username=session['username'])
    else:
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('home'))

def check_credentials(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username=?", (username,))
    stored_password = cursor.fetchone()
    conn.close()
    
    if stored_password is None:
        return False
    
    return password == stored_password[0]

def add_user_to_db(username, email, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Check if the username or email already exists
    cursor.execute("SELECT * FROM users WHERE username=? OR email=?", (username, email))
    existing_user = cursor.fetchone()
    
    if existing_user:
        if existing_user[1] == username:
            flash('User with this username already exists.', 'error')
        else:
            flash('User with this email address already exists.', 'error')
    else:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                      (username, email, password))
        conn.commit()
    
    conn.close()

def validate_email(email):
    import re
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

if __name__ == '__main__':
    app.run(debug=True)