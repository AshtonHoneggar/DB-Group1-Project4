#################################################################################
# users table
#################################################################################
create_user = "CREATE TABLE IF NOT EXISTS users(" \
              "id        INTEGER PRIMARY KEY AUTOINCREMENT," \
              "firstname TEXT    NOT NULL," \
              "lastname  TEXT    NOT NULL," \
              "role      TEXT    NOT NULL," \
              "username  TEXT    UNIQUE NOT NULL," \
              "password  TEXT    NOT NULL)"

login_user = "SELECT * FROM users WHERE username=?"

register_user = "INSERT INTO users(firstname, lastname, role, username, password) VALUES (?,?,?,?,?);"

#################################################################################
# tickets table
#################################################################################
create_ticket = "CREATE TABLE IF NOT EXISTS tickets(" \
                "id           INTEGER PRIMARY KEY AUTOINCREMENT," \
                "reported_by  TEXT    NOT NULL," \
                "issue        TEXT    NOT NULL," \
                "status       TEXT    NOT NULL," \
                "user_comment TEXT    NOT NULL," \
                "IT_comment   TEXT," \
                "date_opened  DATE    NOT NULL," \
                "date_closed  DATE)"

new_ticket = "INSERT INTO tickets(issue, user_comment, date_opened, reported_by, status) VALUES (?,?,?,?,'open');"

open_ticket = "SELECT * FROM tickets WHERE date_closed=NULL"

close_ticket = "UPDATE tickets SET status=?, it_comment=?, date_closed=? WHERE id=?"

ticket_status = "UPDATE tickets SET status=? WHERE id=?"

#################################################################################
# assigned table
#################################################################################
create_assigned = "CREATE TABLE IF NOT EXISTS assigned (" \
                  "reported_by TEXT    NOT NULL," \
                  "assigned_to TEXT," \
                  "ticket_id   INTEGER NOT NULL)"

assign_report = "INSERT INTO assigned(reported_by, ticket_id) VALUES (?,?);"

assign_it = "UPDATE assigned SET assigned_to=? WHERE ticket_id=?"

assigned_ticket = "SELECT * FROM tickets T, assigned A WHERE (A.assigned_to=? OR A.reported_by=?) AND A.ticket_id=T.id ORDER BY T.date_opened DESC"

unassigned_ticket = "SELECT * FROM tickets t EXCEPT SELECT t.* FROM tickets t, assigned a WHERE a.ticket_id=t.id AND a.assigned_to IS NOT NULL"
