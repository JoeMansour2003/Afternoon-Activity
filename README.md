# Afternoon Activity Website for Camp Transfiguration

The goal is to simplify and automate the way campers receive and pick afternoon activities.


### Camp Transfiguration Afternoon Activity Site 
[http://staff.camptransfiguration.org](http://staff.camptransfiguration.org)

### Camp Transfiguration Site
[https://www.camptransfiguration.org](https://www.camptransfiguration.org)

## Activity Selector Page
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/0cff979e-c708-4157-b458-601f13f4534e">

## Cabin View Page
<img width="1352" alt="Screenshot 2024-09-20 at 7 00 29 PM" src="https://github.com/user-attachments/assets/c8eb348d-0721-4d74-b25b-d9df054b8e70">

## Camper Activity Selection Page
<img width="987" alt="Screenshot 2024-09-20 at 7 05 41 PM" src="https://github.com/user-attachments/assets/61a9d6ba-c58d-4e3f-ba03-480a880dd804">
<img width="302" alt="Screenshot 2024-09-20 at 7 07 20 PM" src="https://github.com/user-attachments/assets/b59505cc-d697-4f10-bdd5-39a7ce7d4acf">

## Campers For Selected Activity View
<img width="1330" alt="Screenshot 2024-09-20 at 7 10 09 PM" src="https://github.com/user-attachments/assets/cea87a21-1470-4e8f-8b58-71a4dff20583">


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

Create Django admin

    python3 manage.py createsuperuser
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
