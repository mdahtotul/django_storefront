# Current Dir
Code With Mosh - The Ultimate Django Series (Part 2)\2 Building RESTful APIs with Django REST Framework\

# Last Tutorial

10- Creating Custom Serializer Fields

# Re-check: lesson


# Setup django project with pipenv
## Step-1: Install & Check pipenv

If pipenv is not installed in your computer run `pip install pipenv`
After install Run `pip --version` to check if pipenv installed successfully or not.

![output](https://i.ibb.co/tK5p6Bg/1.png)

## Step-2: .venv folder

Go to your project director. Then create a folder name `.venv` in your project directory.
Remember it is important to create `.venv` in your project directory otherwise project requirement packages will install in other location.

![output](https://i.ibb.co/z6XbBmq/2.png)

## Step-3: Create Virtual Environment & Pipfile

Run `pipenv shell`
This will create virtual environment inside `.venv` folder, also create a Pipfile

![output](https://i.ibb.co/zf4kNH8/3.png)

## Step-4: Install Django

Run `pipenv install django`

- This will install django in your project
- add django version to Pipfile
- generate a Pipfile.lock

![output](https://i.ibb.co/hCQYH90/4.png)

## Step-5: Activate VE(virtual environment)

Run `.\.venv\Scripts\activate`
This will activate virtual environment

![output](https://i.ibb.co/DVyrsrJ/5.png)

## Step-6: Run Server

Run `python manage.py runserver 9000`
This will start server on localhost 9000

## Step-7: Create core folder 

Run `django-admin startproject core .`
This will create the main folder for django project.

## Step-8: Create sub-app

Run `python manage.py startapp <YOUR_APP_NAME>`
This will create another app name `YOUR_APP_NAME`

## Step-9: Migrations Statement

Run `python manage.py makemigrations`
This will convert the model class into SQL statements. Create a file inside the Applications's migrations folder which will contain SQL statements.

## Step-10: Execute Migrations Statement

Run `python manage.py migrate`
This will execute the SQL statements generated by makemigrations command and create necessary tables from models.py file

## Step-11: Deactivate VE

Run `deactivate` to stop virtual environment

![output](https://i.ibb.co/MgmsjVs/6.png)

## Conclusion:

After installing everything successfully your project directory will look like this

![output](https://i.ibb.co/R3znwSQ/7.png)
