# x in a row

This is a simple browser based implementation of the game "four in a row" but variable in win length.

## Installation

### Requirements
- Python 3
- pip

It is recommended to use a virtual python environment (virtualenv).

### Setup
- Install requirements `pip install -r requirements/development.txt`
- Change into the directory `django`
- Run `manage.py migrate` when running for the first time or when updating
- Create an admin user `manage.py createsuperuser` (optional)
- Run local server `manage.py runserver`

### Notes
In this early development version you will have to create new users through the django admin interface `localhost:8000/admin` and also log in through this page. The game itself including the users in it have to be created manually
