# Clinic API 

## Features
- User Management:
Register a new user (Junior role by default).
Log in with username and password to obtain a JWT token.
Promote/Demote user roles (Junior <-> Senior)

- Case Management:
Add new therapy cases with description.
Fetch all existing therapy cases.

- Authentication:
JWT-based authentication to protect endpoints
Only authenticated users can access case and user role management endpoints.


## Tech stack
- Backend: Flask, Flask-RESTX
- Database: SQLite with SQLAlchemy
- Authentication: Flask-JWT-Extended

## Setup
1. Clone repo
git clone https://github.com/shngxng/api-proj.git
cd api-proj

2. set up virtual env
python3 -m venv myenv
source myenv/bin/activate  

3. install dependencies
pip install -r requirements.txt

4. initialise database
flask db init
flask db migrate -m "initial migration"
flask db upgrade

5. Start the development server
flask run

**Deployment on Render:**
API accessible at: https://clinic-api-j0nm.onrender.com/

**API testing example through Postman**
1. POST method: https://clinic-api-j0nm.onrender.com/auth/login

2. Insert Body (Raw in JSON format):
{
  "username": "joel87",
  "password": ""
}

3. Response should read welcome message. 

4. Test POST method for inserting a new case: https://clinic-api-j0nm.onrender.com/therapy/case
    - Copy Access token
    - Add Authorization, Auth Type = Bearer Token and paste access token
    - Insert Body (Raw in JSON format):
{
  "name": "noelle",
  "description": "Testing"
}



## Implementation 

### Program structure 
api-proj/ \
|-- app \
|   |-- __init__.py \
│   |-- models.py          # Database models for  User and Case \
│   |-- services/          # Business logic for authentication and case management \
│   │   |-- user_service.py \
│   │   |__ case_service.py \
│   |-- routes/            # RESTful API routes \
│   │   |-- auth.py \
│   │   |__ cases.py \
│   |__ migrations/ \
|-- requirements.txt \
|-- run.py \
|__ README.md 

**Database Models (app/models.py)**
- User: Stores user credentials and roles (Junior / Senior).
- Case: Therapy cases.

**Services (app/services/)**
- user_service.py: Handles user registration, login, promotion, and demotion.
- case_service.py: Handles fetching and adding therapy cases.

**Routes (app/routes/)**
- auth.py: Authentication endpoints (/auth/*).
    1. /auth/register (POST): Register a user with username and password.
    2. /auth/login (POST): Authenticates a user with username and password.
    3. /auth/promote (POST):Promote a user from "Junior" to "Senior" with username and password. If the user is already "Senior", return a message accordingly.
    4. /auth/demote (POST): Demote a user from "Senior" to "Junior" with username and password. If the user is already "Junior", return a message accordingly.

- cases.py: Therapy case endpoints (/therapy/*).
    1. /therapy/cases (GET): Fetch the list of all cases.
    2. /therapy/case (POST): Adds a case.

