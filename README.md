# Installation setup for contributors
## Requirements
- python 3.9.1
- pip 3
- mysql database
- virtualenv
    - can be installed using `pip install virtualenv`

## Install Instructions

1. clone the repo
2. create a new git branch using the master branch  
    `git checkout -b [your_name]`
3. install dependencies   
    `pip install -r requirements.txt`
4. create a database called "crossline" in your mysql install
5. create a .env file in the root directory and add
    ```
    DATABASE_NAME=crossline
    DATABASE_USER=root
    DATABASE_PASSWORD=''
    DATABASE_HOST='localhost'
    DATABASE_PORT='3306'
    ```
    make sure to edit the values to match your database settings
6. make migrations   
    `python manage.py makemigrations`
7. migrate   
    `python manage.py migrate`
8. make sure your database now has the below tables  
    ```
    auth_group
    auth_group_permissions
    auth_permission
    auth_user
    auth_user_groups
    auth_user_user_permissions
    bus_bus
    busschedule_busschedule
    busschedule_datetype
    busschedule_schedulesetting
    busstop_busstop
    django_admin_log
    django_content_type
    django_migrations
    django_session
    ```
9. create a new superuser for the project eg.   
    `python manage.py createsuperuser admin`   
    this will guide you in creating a super user with the username "admin"
10. Run the dev server `python manage.py runserver`
11. you should now be able to login using the super user account
12. in order to have the same groups/user types, run the groups.sql file in your database, make sure to read the comments.
13. you should be able to start coding your modules after all the above is done

## Push requests

Note that when pushing to the repo, you will need to push your branch **not** the master branch