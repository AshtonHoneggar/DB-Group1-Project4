import os
import sqlite3 as sql
import sys
import uuid
from os.path import join, dirname
from flask import Flask, request, Response, json, jsonify, render_template
from time import gmtime, strftime

app = Flask(__name__, template_folder='static')
app.config['DEBUG'] = True

if __name__ == "__main__":
    app.run(port=5000)


#Route for /
@app.route("/")
def main():
    return render_template('/index.html')

#Make SQL cursor return dictionary
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

#################################################################################
# login/register
#################################################################################
@app.route('/login', methods=['POST'])
def login():
    user = request.form['username']
    password = request.form['password']
    con = sql.connect("ITsupport.db", timeout=10)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE username=?", user)
    temp = cur.fetchone()
    cur.close()
    #if user and password are not in users table, error message appears
    if user == temp["username"] and password == temp["password"]:
        return jsonify({
            'auth': True,
            'user': {
                "username": user,
                "firstName": temp["firstname"],
                "lastName": temp["lastname"], 
                "role": temp["role"]
            }
        })
    else:
        return jsonify({
            'auth': False
        })

#Post request method for /register
@app.route('/register', methods=['POST'])
def register():
    first = request.form['firstreg']
    last = request.form['lastreg']
    email = request.form['emailreg']
    role = request.form['rolereg']
    user = request.form['userreg']
    password = request.form['passwordreg']
    passwordconf = request.form['passwordconfreg']
    con = sql.connect("ITsupport.db", timeout=10)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("CREATE TYPE USER_ROLE AS ENUM ('user', 'it')")
    cur.execute("CREATE TABLE IF NOT EXISTS users("
                "id              SERIAL             PRIMARY KEY,"
                "firstname       VARCHAR(64)        NOT NULL,"
                "lastname        VARCHAR(64)        NOT NULL,"
                "email           VARCHAR(64)        NOT NULL,"
                "role            USER_ROLE          NOT NULL DEFAULT 'user',"
                "username        VARCHAR(64)        UNIQUE NOT NULL,"
                "password        VARCHAR(64)        NOT NULL)")
    if password == passwordconf:
        cur.execute("INSERT INTO users(firstname, lastname, email, role, username, password) VALUES (?,?,?,?,?,?);", (first, last, email, role, user, password))
        con.commit()
        cur.close()
        con.close()
        return jsonify({
            'registered': True
        })

#################################################################################
# Tickets/assigned
#################################################################################
@app.route('/getTickets', methods=['GET'])
def getOpenTickets():
    con = sql.connect("ITsupport.db", timeout=10)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("CREATE TYPE TICKET_STATUS AS ENUM('open', 'in_progress', 'closed')")
    cur.execute("CREATE TYPE ISSUE_TYPE AS ENUM('other', 'hardware', 'software')")
    cur.execute("CREATE TABLE IF NOT EXISTS tickets("
                "id              SERIAL             PRIMARY KEY,"
                "reported_by     varchar(64)        REFERENCES users (username) ON DELETE CASCADE NOT NULL,"
                "issue           ISSUE_TYPE         NOT NULL DEFAULT 'other',"
                "status          TICKET_STATUS      NOT NULL DEFAULT 'open',"
                "user_comment    VARCHAR(64)        NOT NULL,"
                "IT_comment      VARCHAR(64)        NOT NULL,"
                "date_opened     Date               NOT NULL,"
                "date_closed     Date)")
    cur.execute("SELECT * FROM tickets WHERE date_closed=NULL")
    ticketdata = cur.fetchall()
    con.commit()
    cur.close()
    con.close()
    return jsonify({
        'opentickets': ticketdata
    })

@app.route('/newTicket', methods=['POST'])
def newTicket():
    user = request.args.get("temp")
    issue = request.form['issuetix']
    comment = reqest.form['commenttix']

    con = sql.connect("ITsupport.db", timeout=10)
    con.row_factory = dict_factory
    cur = con.cursor()
    #TODO: sqlite3 does not like create type as enum, if all else fails make a drop down box on front end
    # cur.execute("CREATE TYPE TICKET_STATUS AS ENUM('open', 'in_progress', 'closed')")
    # cur.execute("CREATE TYPE ISSUE_TYPE AS ENUM('other', 'hardware', 'software')")
    cur.execute("CREATE TABLE IF NOT EXISTS tickets("
                "id              SERIAL             PRIMARY KEY,"
                "issue           ISSUE_TYPE         NOT NULL DEFAULT 'other',"
                "status          TICKET_STATUS      NOT NULL DEFAULT 'open',"
                "user_comment    VARCHAR(64)        NOT NULL,"
                "IT_comment      VARCHAR(64),"
                "date_opened     VARCHAR(64)               NOT NULL,"
                "date_closed     VARCHAR(64))")
    cur.execute("CREATE TABLE IF NOT EXISTS assigned ("
                "reported_by     varchar(64) REFERENCES users (username) ON DELETE CASCADE   NOT NULL,"
                "assigned_to     varchar(64) REFERENCES users (username) ON DELETE CASCADE,"
                "ticket_id       INTEGER REFERENCES tickets (id) ON DELETE CASCADE NOT NULL)")
    cur.execute("INSERT INTO tickets(issue, user_comment, date_opened) VALUES (?,?,?);", (issue, comment, strftime("%Y-%m-%d", gmtime())))
    ticketID = cur.lastrowid
    con.commit()
    cur.execute("INSERT INTO assigned(reported_by, ticket_id) VALUES (?,?)", (user, ticketID))
    con.commit()
    cur.close()
    con.close()
    return jsonify({
       'newticket': True
    })

@app.route('/assignTicket', methods=['POST'])
def assignTicket():
    user = request.args.get("temp")
    # TODO: how do we get ticketID of the ticket being assigned to?
    # ticketID = getTicketID()
    con = sql.connect("ITsupport.db", timeout=10)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS assigned ("
                "reported_by     varchar(64) REFERENCES users (username) ON DELETE CASCADE   NOT NULL,"
                "assigned_to     varchar(64) REFERENCES users (username) ON DELETE CASCADE,"
                "ticket_id       INTEGER REFERENCES tickets (id) ON DELETE CASCADE NOT NULL)")
    cur.execute("UPDATE assigned SET assigned_to=? WHERE ticket_id", (user, ticketID))
    con.commit()
    cur.close()
    con.close()
    return jsonify({
       'assign_it': True
    })

@app.route('/status', methods=['POST'])
def ticketStatus():
    status = request.form['tixstatus']
    comment = request.form['closecomment']
    # TODO: how do we know which ticket is being changed?
    # ticketID = getTicketID()
    con = sql.connect("ITsupport.db", timeout=10)
    con.row_factory = dict_factory
    cur = con.cursor()
    # TODO: if else can be list comprehension but i forget format
    if status == 'open':
        cur.execute("UPDATE ticket SET status=? WHERE ticket_id", (status, ticketID))
    elif status == 'in_progress':
        cur.execute("UPDATE ticket SET status=? WHERE ticket_id", (status, ticketID))
    elif status == 'closed':
        # TODO: need a way to get the IT comment
        cur.execute("UPDATE ticket SET status=?, it_comment=?, date_closed=? WHERE ticket_id=?", (status, comment, strftime("%Y-%m-%d", gmtime()), ticketID))
    else:
        return jsonify({
            # ajax return failed to update status
            'ticketstatus': False
        })
    con.commit()
    cur.close()
    con.close()
    return jsonify({
       'ticketstatus': True
    })