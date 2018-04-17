import schema
import sqlite3 as sql
from flask import Flask, request, session, jsonify, render_template
from time import gmtime, strftime


app = Flask(__name__, template_folder='static')
app.config['DEBUG'] = True

if __name__ == "__main__":
    app.run(port=5000)


# Make SQL cursor return dictionary
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

#################################################################################
# main
#################################################################################


@app.route("/")
def main():
    return render_template('/index.html')

#################################################################################
# login/register
#################################################################################


@app.route('/login', methods=['POST'])
def login():
    user = request.form['username']
    password = request.form['password']
    con = sql.connect("ITsupport.db")
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute(schema.login_user, (user,))
    temp = cur.fetchone()
    cur.close()
    # if user and password are not in users table, error message appears
    if user == temp['username'] and password == temp['password']:
        session['username'] = user
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


@app.route('/register', methods=['POST'])
def register():
    first = request.form['firstreg']
    last = request.form['lastreg']
    role = request.form['rolereg']
    user = request.form['userreg']
    password = request.form['passwordreg']
    passwordconf = request.form['passwordconfreg']
    con = sql.connect("ITsupport.db", timeout=10)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute(schema.create_user)
    if password == passwordconf:
        cur.execute(schema.register_user, (first, last, role, user, password))
        con.commit()
        cur.close()
        con.close()
        return jsonify({
            'registered': True
        })
    else:
        return jsonify({
            'registered': False
        })

#################################################################################
# Tickets/assigned
#################################################################################


@app.route('/getTickets', methods=['POST'])
# used for IT to get all open tickets, use /getAssigned to return your tickets
def get_open_tickets():
    con = sql.connect("ITsupport.db", timeout=10)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute(schema.create_ticket)
    cur.execute(schema.open_ticket)
    open_data = cur.fetchall()
    con.commit()
    cur.close()
    con.close()
    return jsonify({
        'opentickets': open_data
    })


@app.route('/getAssigned', methods=['POST'])
def get_assigned_tickets():
    user = session['username']
    con = sql.connect("ITsupport.db", timeout=10)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute(schema.create_ticket)
    cur.execute(schema.create_assigned)
    cur.execute(schema.assigned_ticket, (user, user))
    assigned_data = cur.fetchall()
    con.commit()
    cur.close()
    con.close()
    return jsonify({
        'assignedtickets': assigned_data
    })

@app.route('/getUnassigned', methods=['POST'])
def get_unassigned_tickets():
    user = session['username']
    con = sql.connect("ITsupport.db", timeout=10)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute(schema.create_ticket)
    cur.execute(schema.create_assigned)
    cur.execute(schema.unassigned_ticket)
    unassigned_data = cur.fetchall()
    con.commit()
    cur.close()
    con.close()
    return jsonify({
        'unassignedtickets': unassigned_data
    })

@app.route('/newTicket', methods=['POST'])
def new_ticket():
    user = session['username']
    issue = request.form['ticketType']
    comment = request.form['commenttix']
    con = sql.connect("ITsupport.db", timeout=10)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute(schema.create_ticket)
    cur.execute(schema.create_assigned)
    cur.execute(schema.new_ticket, (issue, comment, strftime("%Y-%m-%d", gmtime()), user))
    ticket_id = cur.lastrowid
    con.commit()
    cur.execute(schema.assign_report, (user, ticket_id))
    con.commit()
    cur.close()
    con.close()
    return jsonify({
       'newticket': True
    })
    


@app.route('/assignTicket', methods=['POST'])
def assign_ticket():
    user = session['username']
    # IT inputs ticket id to assign them to it
    ticket_id = request.form['assigntix']
    con = sql.connect("ITsupport.db", timeout=10)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute(schema.ticket_status, ("in progress", ticket_id))
    con.commit()
    cur.execute(schema.assign_it, (user, ticket_id))
    con.commit()
    cur.close()
    con.close()
    return jsonify({
       'assign_it': True
    })


@app.route('/closeTicket', methods=['POST'])
def close_ticket():
    ticket_id = request.form['closetix']
    ticket_conf = request.form['closetixconf']
    comment = request.form['closecomment']

    con = sql.connect("ITsupport.db", timeout=10)
    con.row_factory = dict_factory
    cur = con.cursor()
    if ticket_id == ticket_conf:
        cur.execute(schema.close_ticket, ("closed", comment, strftime("%Y-%m-%d", gmtime()), ticket_id))
        con.commit()
        cur.close()
        con.close()
        return jsonify({
            'closed': True
        })
    else:
        cur.close()
        con.close()
        return jsonify({
            'closed': False
        })

    
@app.route('/logout', methods=['POST'])
def logout():
    return jsonify({
       'isUser': True
    })
    
app.secret_key = 'A0Zr98j/3yX R~X0H!jmN]LWX/,?RT'
