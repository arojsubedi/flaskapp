import sys
from flask import Flask,render_template
from flask import request
from flaskext.mysql import MySQL

app = Flask(__name__,template_folder='./')

# Configure the connection to your Amazon RDS database
app.config['MYSQL_DATABASE_HOST'] = 'myprojectdb.co9cbtnukhck.us-east-1.rds.amazonaws.com'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'adminadmin'
app.config['MYSQL_DATABASE_DB'] = 'users'


# Initialize the MySQL connection
mysql = MySQL(app)
mysql.init_app(app)

@app.route('/',methods=['GET','POST'])
def index():
        return render_template("loginpage.html")

@app.route('/registration/',methods=['GET','POST'])
def registration():
        return render_template("index.html")

@app.route('/register/',methods=['POST'])
def register():
        msg = ""
        if request.method == 'POST' and 'Username' in request.form and 'Password' in request.form and 'FirstName' in request.form and 'LastName' in request.form and 'Email' in request.form:
                username = request.form['Username']
                password = request.form['Password']
                firstname = request.form['FirstName']
                lastname = request.form['LastName']
                email = request.form['Email']
                print(email,file=sys.stderr)
                print(username,file=sys.stderr)
                if username == '' or password == '' or firstname == '' or lastname == '' or email == '':
                        msg = "Missing details. Please enter all the details"
                        return render_template('./index.html',msg=msg)

                cursor = mysql.get_db().cursor()
                cursor.execute("SELECT * FROM users where username = %s and password = %s",(username,password))
                data = cursor.fetchone()
                cursor.close()
                if data is None:
                        cursor=mysql.get_db().cursor()
                        cursor.execute("INSERT INTO users (username, password, firstname, lastname, email) VALUES (%s, %s, %s, %s, %s);",(username,password,firstname,lastname,email))
                        mysql.get_db().commit()
                        msg = 'User registered successfully'
                        cursor.close()
                        return render_template('./loginpage.html',msg=msg)
                else:
                        msg = "username already present. please log in"
                        return render_template('./loginpage.html',msg=msg)


@app.route('/login/', methods=['POST'])
def login():
        msg=""
        fn=""
        ln=""
        email=""
        if request.method == 'POST' and 'Username' in request.form and 'Password' in request.form:
                username = request.form['Username']
                password = request.form['Password']
                cursor = mysql.get_db().cursor()
                cursor.execute("SELECT * FROM users where username = %s and password = %s",(username,password))
                data = cursor.fetchone()

                if data is None:
                        msg = "username or password incorrect or user not registered"
                        return render_template('./index.html',msg=msg)

                else:
                        fn = data[2]
                        ln = data[3]
                        email = data[4]
                        msg = 'User found'
                        return render_template('./userdetails.html',msg=msg,fn=fn,ln=ln,email=email)


@app.route("/loginpage")
def loginpage():
        return render_template("loginpage.html")

if __name__ == '__main__':
  app.run()

