This is the Afternoon Activity website for Camp Transfiguration

The goal is to simplify and automate the way campers receive and pick afternoon activities.

### SuperUser info:

Username:
admin
<br>
Password:
campt
<br>
Email:
joemansour2003@gmail.com


# Dev Notes

### Theme
If you make any changes to the custom colours run the following command in the `sass afternoon_activity/static/afternoon_activity/scss/custom.scss afternoon_activity/static/afternoon_activity/scss/custom.css`
or if you are in the path just do
`sass custom.scss custom.css`


command to drop all tables:

    DO $$ DECLARE
        r RECORD;
    BEGIN
        FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
            EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
        END LOOP;
    END $$;


RUN SERVER 24/7 
    nohup python3 manage.py runserver 0.0.0.0:8000 &
on the server

to list all running instances do 
    ps aux | grep manage.py

you end up getting
    ec2-user  37905  0.5  2.0  100000  12345 pts/0  S  00:00  0:05 python3 manage.py runserver 0.0.0.0:8000
    ec2-user  37908  0.0  0.0  10540    920 pts/0  S  00:00  0:00 grep manage.py

To kill a process you need to do 
    Kill <pID>
    ex: Kill 37905