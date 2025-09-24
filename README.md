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
- Add bew enrollments via a dedicated form
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
├─ static/                # Static assets
│   └─ style.css
│
├─ templates/             # HTML templates, organized by type
│   ├─ add_*.html
│   ├─ edit_*.html
│   ├─ dashboard_*.html
│
├─ screenshots/
│   ├─ add_course.jpg
│   ├─ add_enrollment.jpg
│   ├─ add_student.jpg
│   ├─ courses_dashboard.jpg
│   ├─ edit_course.jpg
│   ├─ edit_enrollment.jpg
│   ├─ edit_student.jpg
│   ├─ enrollments_dashboard.jpg
│   ├─ log_out.jpg
│   ├─ login_dashboard.jpg
│   ├─ search_function.jpg
│   ├─ statistics.jpg
│   └─ student_dashboard.jpg
└─ venv/                  # Virtual environment
```
Note: The modules/ folder centralizes all SQL query functions. Templates are divided by function: add, edit, or dashboard.
## Setup Instructions

1. **Clone the repository:**

```bash
git clone https://github.com/<USERNAME>/<REPO>.git
cd student_project
```
Create and activate a virtual environment:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```
Install dependencies:

```bash
pip install -r requirements.txt
```
Create a .env file in the root with your database credentials (password is not stored, it will be entered at login):
```bash
DB_HOST=localhost
DB_NAME=student_db
```
Generate self-signed SSL certificates (required for HTTPS):

```bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```
Update the paths in app.py to match the location of your generated certificates:
```bash
if __name__ == "__main__":
    # Make sure to generate self-signed certificates first
    # openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
    app.run(ssl_context=(
        r"YOUR_LOCAL_PATH_TO\cert.pem",
        r"YOUR_LOCAL_PATH_TO\key.pem"
    ), debug=True)
Replace YOUR_LOCAL_PATH_TO with the actual path where your cert.pem and key.pem files are located.
```
Run the application:
```bash
python app.py
```
Open your browser at https://localhost:5000 (or http://localhost:5000 if HTTPS is not configured)




## Screenshots

### Login
![Login Dashboard](screenshots/login_dashboard.jpg)

### Student Dashboard
![Student Dashboard](screenshots/student_dashboard.jpg)

### Courses Dashboard
![Courses Dashboard](screenshots/courses_dashboard.jpg)

### Enrollments Dashboard
![Enrollments Dashboard](screenshots/enrollments_dashboard.jpg)

### Add / Edit Forms
![Add Student](screenshots/add_student.jpg)
![Add Course](screenshots/add_course.jpg)
![Add Enrollment](screenshots/add_enrollment.jpg)
![Edit Student](screenshots/edit_student.jpg)
![Edit Course](screenshots/edit_course.jpg)
![Edit Enrollment](screenshots/edit_enrollment.jpg)

### Features
![Search Function](screenshots/search_function.jpg)
![Statistics](screenshots/statistics.jpg)
![Log Out](screenshots/log_out.jpg)

