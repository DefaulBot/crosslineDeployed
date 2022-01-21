# Requirements
- python 3.9.1
- pip 3
- mysql database
- virtualenv
    - can be installed using `pip install virtualenv`

# Install Instructions

1. create a new virtual environment for the django project   
    `$ virtualenv [folder name]`

2. copy this project into the new virtual environment folder created at step 1

3. install dependencies, run the command within this project folder   
    `$ pip install -r requirements.txt`

4. create a database called "crossline" in your mysql install

5. create a .env file in the root directory of this project and add the following environment variables
    ```
    DATABASE_NAME=crossline
    DATABASE_USER=root
    DATABASE_PASSWORD=''
    DATABASE_HOST='localhost'
    DATABASE_PORT='3306'
    ```
    make sure to edit the values to match your database settings

6. activate your virtual environment   
    - within your virtual environment folder created at step 1 run the following command   
    `$ source scripts/activate`   
    or simply run the scripts/activate script relevant to your preferred shell(cmd, powerhsell, bash)

6. create the migration files using the below command   
    `$ python manage.py makemigrations`

7. now run the migrations using the below command 
    `$ python manage.py migrate`

8. make sure your database has been populated with the below tables
    ```
    auth_group
    auth_group_permissions
    auth_permission
    auth_user
    auth_user_groups
    auth_user_user_permissions
    bus_bus
    busrun_busrun
    busrun_busstop_in_busrun
    busrun_busstop_to_busstop
    busrun_location
    django_admin_log
    django_content_type
    django_migrations
    django_session
    ticket_ticket
    ```

9. create a new superuser for the project eg.   
    `$ python manage.py createsuperuser --username admin`   
    this will guide you in creating a super user with the username "admin"

10. Run the development server    
`$ python manage.py runserver`

11. login using the super user account at http://localhost:8000/


## Django project structure
- template files can be found within the views/ directory
- static files can be found within the static/ directory
- app_name/urls.py files contain application routes
- app_name/forms.py files contain code relevant to forms used within the relevant app
- app_name/views.py contain the route handlers, they prepare the data for presentation within the templates
- app_name/models.py contain model mappings for the tables in the database 