from flask import Flask, render_template, request,session, redirect, url_for, flash
from flaskext.mysql import MySQL
import pymysql
import re
app = Flask(__name__)
app.secret_key = "Pipat"

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'PATIENT_APPOINTMENT'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


# http://localhost:5000/pythonlogin/ - this will be the login page
@app.route('/login/', methods=['GET', 'POST'])
def login():
 # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
  
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
        # Fetch one record and return result
        account = cursor.fetchone()
   
    # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['Uid'] = account['Uid']
            session['username'] = account['username']
            # Redirect to home page
            #return 'Logged in successfully!'
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    
    return render_template('index.html', msg=msg)

# http://localhost:5000/register - this will be the registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
 # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
  
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
   
  #Check if account exists using MySQL
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s, %s)', (fullname, username, password, email)) 
            conn.commit()
   
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)
  
# http://localhost:5000/home - this will be the home page, only accessible for loggedin users
@app.route('/')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
   
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
        return render_template('home.html', Uid=session['Uid'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/logout - this will be the logout page
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))
 
# http://localhost:5000/profile - this will be the profile page, only accessible for loggedin users
@app.route('/profile')
def profile(): 
 # Check if account exists using MySQL
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
  
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor.execute('SELECT * FROM accounts WHERE Uid = %s', [session['Uid']])
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


###################################################################################
###################################################################################

@app.route('/appo')
def Index():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM appo_list Where Uid = %s', [session['Uid']])
    data = cur.fetchall()

    cur.close()
    return render_template("appo.html", appo_list = data)

#หน้าโฮม
#    cur.execute('SELECT * FROM accounts WHERE Uid = %s', [session['Uid']])
@app.route("/add_appo", methods=['POST'])
def add_appo():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        P_name = request.form['P_name']
        detail = request.form['detail']
        room = request.form['room']
        status = request.form['status']
        date = request.form['date']
        Uid = session['Uid']
        cur.execute("INSERT INTO appo_list(P_name, detail, room, status, date, Uid) VALUES(%s, %s, %s, %s, %s, %s)", (P_name, detail, room, status, date, Uid))
        conn.commit()
        flash(' Patient appointment added successfully')
        return redirect(url_for('home'))

@app.route("/edit/<Pid>", methods=['POST', 'GET'])
def get_appo(Pid):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute("SELECT * FROM appo_list WHERE Pid = %s", (Pid))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit.html', appo_list = data[0])

@app.route("/update/<Pid>", methods=['POST'])
def update_appo(Pid):
    if request.method == 'POST':
        P_name = request.form['P_name']
        detail = request.form['detail']
        room = request.form['room']
        status = request.form['status']
        date = request.form['date']
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("""
            UPDATE appo_list
            SET P_name = %s,
                detail = %s,
                room = %s,
                status = %s,
                date = %s
            WHERE Pid = %s
        """, (P_name, detail, room, status,date, Pid))
        flash('Appointment Updated Successfully')
        conn.commit()
        return redirect(url_for('Index'))

@app.route("/delete/<string:Pid>", methods=["POST", "GET"])
def delete_appo(Pid):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute('DELETE FROM appo_list WHERE Pid = {0}'.format(Pid))
    conn.commit()
    flash("Friend Removed Successfully")
    return redirect(url_for('Index'))

  
#starting the app
if __name__ == "__main__":
    app.run(port=3000, debug=True)
