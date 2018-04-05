--This file populates the tables

--Populate users table
Insert into users (firstname, lastname, email, username, password) 
values ('personA', 'personA', 'personA@gmail.com', 'pA', 'PassA' );

Insert into users (firstname, lastname, email, username, password) 
values ('Mike', 'personB', 'Mike@gmail.com', 'Mike', 'MikePass' );

Insert into users (firstname, lastname, email, role, username, password) 
values ('Itperson', 'Itperson', 'IT@yahoo.com', 'it', 'IT', 'ITPass' );

Insert into users (firstname, lastname, email, role, username, password) 
values ('Itperson2', 'Itperson2', 'IT2@yahoo.com', 'it', 'IT2', 'IT2Pass' );

--Populate tickets table

Insert into tickets (reported_by,user_comment, IT_comment, date_opened, date_closed)
values ('Mike','Problems with computer', 'User doesnt know how to turn on computer', '2018-03-12', '2018-04-12');

Insert into tickets (reported_by, issue, status, user_comment, IT_comment, date_opened, date_closed)
values ('Mike','software', 'closed', 'Problems with computer', 'User doesnt know how to turn on computer', '2018-03-11', '2018-04-11');

Insert into tickets (reported_by, issue, status, user_comment, IT_comment, date_opened)
values ('Mike','software', 'in_progress', 'Problems', 'asdf', '2018-03-11');

Insert into tickets (reported_by, user_comment, IT_comment, date_opened)
values ('Mike','Problems with computer', 'asdf', '2005-03-12');

Insert into tickets (reported_by, issue, status, user_comment, IT_comment, date_opened, date_closed)
values ('Mike','software', 'closed', 'asdf', 'asdf', '2006-03-11', '2007-04-11');

Insert into tickets (reported_by, issue, status, user_comment, IT_comment, date_opened)
values ('Mike','software', 'in_progress', 'Problems', 'asdf', '2018-03-11');

-- Populate assigned table
Insert into assigned (reported_by,ticket_id)
Select reported_by, id from tickets;





