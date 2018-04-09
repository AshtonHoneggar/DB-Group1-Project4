import os
import psycopg2 as sql
import sys
import uuid
from os.path import join, dirname
from flask import Flask, request, Response, json, jsonify, render_template

app = Flask(__name__, template_folder='static')
app.config['DEBUG'] = True

if __name__ == "__main__":
    app.run(port=5000)


#Route for /
@app.route("/")
def main():
    # TODO: initialize the postgres database
    return render_template('/index.html')

#Make SQL cursor return dictionary
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

#Post request method for /login
@app.route('/login', methods=['POST'])
def login():
    user = request.form['username'];
    password = request.form['password'];
    con = sql.connect("dbname='ITsupport' user='postgres' host='localhost' password='password'")
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE username=?", user)
    temp = cur.fetchone()
    cur.close()
    print(temp)
    if email == temp["email"] and password == temp["password"]:
        return jsonify({
            'auth': True,
            'user': {
                "username": user,
                "firstName": temp["firstname"],
                "lastName": temp["lastname"]
            }
        })
    else:
        return jsonify({
            'auth': False
        })

#Post request method for /register
@app.route('/register', methods=['POST'])
def register():
    first = request.form['firstreg'];
    last = request.form['lastreg'];
    email = request.form['emailreg'];
    role = request.form['rolereg'];
    user = request.form['userreg'];
    password = request.form['passwordreg'];
    passwordconf = request.form['passwordconfreg'];
    con = sql.connect("dbname='ITsupport' user='postgres' host='localhost' password='password'")
    con.row_factory = dict_factory
    cur = con.cursor()
    try:
        cur.execute("SELECT * FROM users WHERE email = " + email + ";")
        temp = cur.fetchone()
        print(temp)
    except:
        print("User not found")
    if password == passwordconf:
        uid = str(uuid.uuid4())
        cur.execute("""INSERT INTO users(id, firstname, lastname, email, role, username, password) VALUES (?,?,?,?,?,?,?);""", (uid, first, last, email, role, user, password))
        con.commit()
        cur.close()
        con.close()
        return jsonify({
            'registered': True
        })

#Returns user's open tickets
@app.route('/getTickets', methods=['GET'])
def home():
    #Print json from get request
    print(request.args)
    #Save the email to a variable
    email =  request.args.get("temp");
    print(email)
    con = sql.connect("dbname='ITsupport' user='postgres' host='localhost' password='password'")
    con.row_factory = dict_factory
    cur = con.cursor()
    uid = str(uuid.uuid4())
    # replace with users/it open tickets
    cur.execute("SELECT * FROM users WHERE email=?", email)
    eventdata = cur.fetchall()
    print(eventdata)
    con.commit()
    cur.close()
    con.close()
    return jsonify({
        'events': eventdata
    });


# Example: replace with newTicket
# @app.route('/newEvent', methods=['POST'])
# def newEvent():
#     email = request.form['email']
#     eventName =  request.form['eventName'];
#     eventTime = request.form['eventTime'];
#     eventUrl = request.form['eventUrl'];
#     con = sql.connect("temp.db", timeout=10)
#     con.row_factory = dict_factory
#     cur = con.cursor()
#     # Uncomment the following line to create the table then comment it again after the first registration
#     # cur.execute("CREATE TABLE event(id INT PRIMARY_KEY, email TEXT, eventName TEXT, eventTime TEXT, eventUrl TEXT)")
#     uid = str(uuid.uuid4())
#     cur.execute("""INSERT INTO event(id, email, eventName, eventTime, eventUrl) VALUES (?,?,?,?,?);""", (uid, email, eventName, eventTime, eventUrl))
#     con.commit()
#     cur.close()
#     con.close()
#     return jsonify({
#         'newEventStatus': True
#     })