# Student Management Web Application

A personal project built using **Python, Flask, HTML, CSS, and MySQL** to manage a student database through a web interface. The application allows authenticated users to manage students, courses, enrollments, and view statistics in a secure and user-friendly way.

---

## NOTE

This application requires a MySQL database with **pre-created tables** according to the structure of the web app.  
Make sure the database contains at least the following tables:

- **students**  
  Main columns: `id`, `first_name`, `last_name`, `email`, `dob`, `student_id`

- **courses**  
  Main columns: `id`, `name`, `code`, `teacher`, `credits`

- **enrollments**  
  Main columns: `id`, `student_id`, `course_id`, `registration_date`, `mark`, `status`

> Note: The database **password is not stored in the `.env` file**. It is provided by the user at login, following the secure authentication method implemented in the app. Make sure to create the database and tables before running the application.

## Features

### Authentication
- Login using a **username and database password**  
- Sessions securely managed with **HTTP-only, Secure, and SameSite cookies**  
- Automatic session expiration after **30 minutes of inactivity**  
- Logout functionality available via the navigation bar  

### Dashboard

#### Students Management
- View a table with student details: `ID | First Name | Last Name | Email | DOB | Student ID | Actions`  
- Actions: **Edit** or **Delete** student  
- Add new students via a dedicated form  
- **Search bar** to filter students  

#### Courses Management
- View a table with course details: `ID | Name | Code | Teacher | Credits | Actions`  
- Actions: **Edit** or **Delete** course  
- Add new courses via a dedicated form  
- **Search bar** to filter courses  

#### Enrollments Management
- View a table with enrollment details: `ID | Student ID | Course ID | Registration Date | Mark | Status | Actions`  
- Actions: **Edit** or **Delete** enrollment  
- **Search bar** to filter enrollments  

#### Statistics
- Column chart displaying:  
  - **Number of enrolled students** (blue)  
  - **Number of students who passed** (green)  
  - Fully green column if all students passed a course  

---

## Security
- Database credentials stored securely in a `.env` file (**excluded from Git**)  
- Simulated **HTTPS connection** in local environment with public/private keys  
- **No plaintext passwords**; sessions and authentication handled securely via Flask  
- SQL queries use **parameterized statements** to prevent SQL injection  
- Session security configured with:
```python
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'Lax'
```
Technical Details
Backend: Python + Flask

Frontend: HTML, CSS

Database: MySQL

Database Connection
Managed through db.py, retrieving credentials from session if not explicitly provided

SQL Injection Protection
All database queries use parameterized statements

File Structure
```python
student_project/
│
├─ app.py                 # Main Flask app, routes, and session/security configuration
├─ db.py                  # Database connection helper
├─ .env                   # Environment variables (excluded from Git)
├─ .gitignore             # Excludes sensitive files
├─ cert.pem                # Public key for local HTTPS simulation
├─ key.pem                 # Private key for local HTTPS simulation
│
├─ models/                # Python models for database tables
│   ├─ __init__.py
│   ├─ courses_model.py
│   ├─ enrollment_model.py
│   └─ student_model.py
│
├─ modules/               # Functions to handle SQL queries
│   ├─ student_queries.py
│   ├─ course_queries.py
│   └─ enrollment_queries.py
│
├─ static/                # Static assets
│   └─ style.css
│
├─ templates/             # HTML templates, organized by type
│   ├─ add_*.html
│   ├─ edit_*.html
│   ├─ dashboard_*.html
│
└─ venv/                  # Virtual environment
```
Note: The modules/ folder centralizes all SQL query functions. Templates are divided by function: add, edit, or dashboard.

Setup Instructions
Clone the repository:

```python
git clone https://github.com/<USERNAME>/<REPO>.git
cd student_project
```
Create and activate a virtual environment:

```python
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```
Install dependencies:

```python
pip install -r requirements.txt
```
Create a .env file in the root with your database credentials:
```python
DB_HOST=localhost
DB_USER=root
```
DB_NAME=student_db
Run the application:


python app.py
Open your browser at https://localhost:5000 (or http://localhost:5000 if HTTPS not configured
