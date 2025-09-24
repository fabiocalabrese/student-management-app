from flask import Flask, render_template,request,redirect,url_for,flash,get_flashed_messages,session
from functools import wraps
import secrets
from datetime import timedelta
from models.courses_model import get_all_courses, get_course, add_course, delete_course, update_course
from models.student_model import get_all_students,get_student, add_student, delete_student, update_student
from models.enrollment_model import get_all_enrollments, get_enrollment, update_enroll, delete_enroll, add_enroll, get_enrollment_from_course, get_passed__not_from_course, get_marks_from_enrollments
from db import get_db_connection

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# ---------------------------
# Configurazione sicurezza sessione
# ---------------------------
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,    # Cookie non accessibile da JavaScript
    SESSION_COOKIE_SECURE=True,      # Inviato solo su HTTPS
    SESSION_COOKIE_SAMESITE='Lax'    # Protezione base CSRF
)
app.permanent_session_lifetime = timedelta(minutes=30)  # Sessione scade dopo 30 min di inattività


# ---------------------------
# Middleware: richiede login
# ---------------------------
def login_required(view_func):
    from functools import wraps
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if "username" not in session:
            flash("Please log in to proceed")
            return redirect(url_for("dashboard"))
        return view_func(*args, **kwargs)
    return wrapper


# ---------------------------
# Login
# ---------------------------
@app.route("/", methods=["GET", "POST"])
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        try:
            # Prova connessione DB
            conn = get_db_connection(username, password)
            conn.close()

            # Salva in sessione
            session.clear()  # Previene session fixation
            session["username"] = username
            session["password"] = password
            session.permanent = True

            flash("Login successful!")
            return redirect(url_for("dashboard_students"))

        except Exception:
            flash("Invalid username o password.")
            return redirect(url_for("dashboard"))

    return render_template("dashboard.html")


# ---------------------------
# Logout
# ---------------------------
@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("dashboard"))


# ---------------------------
# Rotte protette
# ---------------------------

@app.route("/students")
@login_required
def dashboard_students():
    query = request.args.get("q", "").strip().lower()
    students = get_all_students()

    if query:
        students = [
            s for s in students
            if query in s["name"].lower() or query in s["surname"].lower() or query in s["student_id"].lower() or query in s["email"].lower()
        ]

    return render_template("dashboard_students.html", students=students)

@app.route("/enrollments")
@login_required
def dashboard_enroll():
    query = request.args.get("q", "").strip().lower()
    enrollments = get_all_enrollments()
    if query:
        enrollments = [
            s for s in enrollments
            if query in s["student_id"].lower() or query in s["course_id"].lower() or query in s["status"].lower()
        ]
    return render_template("dashboard_enrollments.html", enrollments=enrollments)

@app.route("/courses")
def dashboard_courses():
    query = request.args.get("q", "").strip().lower()
    courses = get_all_courses()

    if query:
        courses = [
            c for c in courses
            if query in c["name"].lower() or query in c["teacher"].lower() or query in c["code"].lower()
        ]

    return render_template("dashboard_courses.html", courses=courses)

@app.route('/statistic')
@login_required
def dashboard_statistics():
    stats = get_enrollment_from_course()
    result = get_passed__not_from_course()
    mark = get_marks_from_enrollments()

    course_names = [row['course_name'] for row in stats]
    student_counts = [row['num_students'] for row in stats]
    passed_counts = [row['num_passed'] for row in result]
    not_passed_counts = [row['not_passed'] for row in result]




    return render_template('statistic.html',
                           course_names=course_names,
                           student_counts=student_counts,
                           passed_counts=passed_counts,
                           not_passed_counts=not_passed_counts,
                           )







@app.route("/add/student", methods=["GET", "POST"])
@login_required
def add_student_route():
    if request.method == "POST":
        name = request.form["name"]
        surname = request.form["surname"]
        email = request.form["email"]
        born_date = request.form["born_date"]
        student_id = request.form["student_id"]

        # Usa la funzione dal model
        add_student(name, surname, email, born_date, student_id)
        flash("Student added with success!")
        return redirect(url_for("dashboard_students"))

    else:
        return render_template("add_student.html")

@app.route("/delete/student/<int:id>/<string:student_id>")
@login_required
def delete_student_route(id,student_id):
    delete_student(id,student_id)
    flash("Student deleted with success!")
    return redirect(url_for("dashboard_students"))


@app.route("/edit/student/<int:id>", methods = ["GET","POST"])
@login_required
def edit_student_route(id):
    if request.method == "POST":
        name = request.form["name"]
        surname = request.form["surname"]
        email = request.form["email"]
        born_date = request.form["born_date"]
        student_id = request.form["student_id"]
        old_student_id = request.form["old_student_id"]
        update_student(id,name, surname, email, born_date, student_id,old_student_id)
        flash("Student edited with success!")
        return redirect(url_for("dashboard_students"))

    else:
        student = get_student(id)
        return render_template("edit_student.html", student = student)


@app.route("/add/enroll", methods=["GET", "POST"])
@login_required
def add_enroll_route():
    if request.method == "POST":
        student_id = request.form["student_id"]
        course_id = request.form["course_id"]
        registration_date = request.form["registration_date"]
        mark = request.form["mark"]
        status = request.form["status"]


        add_enroll(student_id, course_id, registration_date, mark, status)
        flash("Enrollment added with success!")
        return redirect(url_for("dashboard_enroll"))

    else:
        return render_template("add_enroll.html")

@app.route("/delete/enroll/<string:student_id>")
@login_required
def delete_enroll_route(student_id):
    delete_enroll(student_id)
    flash("Enrollment deleted with success!")
    return redirect(url_for("dashboard_enroll"))


@app.route("/edit/enroll/<int:id>", methods = ["GET","POST"])
@login_required
def edit_enroll_route(id):
    if request.method == "POST":
        student_code = request.form["student_id"]
        course_id = request.form["course_id"]
        registration_date = request.form["registration_date"]
        mark = request.form["mark"]
        status = request.form["status"]
        update_enroll(id, student_code, course_id, registration_date, mark, status)
        flash("Enrollment edited with success!")
        return redirect(url_for("dashboard_enroll"))

    else:
        enrolled = get_enrollment(id)
        return render_template("edit_enroll.html", enrolled = enrolled)






@app.route("/add/course", methods=["GET", "POST"])
@login_required
def add_course_route():
    if request.method == "POST":
        name = request.form["name"]
        course_id = request.form["course_id"]
        teacher = request.form["teacher"]
        credits = request.form["credits"]

        # Usa la funzione dal model
        add_course(name, course_id, teacher, credits)
        flash("Courses added with success!")
        return redirect(url_for("dashboard_courses"))

    else:
        return render_template("add_course.html")

@app.route("/delete/course/<int:id>/<string:course_id>")
@login_required
def delete_course_route(id,course_id):
    delete_course(id,course_id)
    flash("Course deleted with success!")
    return redirect(url_for("dashboard_courses"))


@app.route("/edit/course/<int:id>", methods = ["GET","POST"])
@login_required
def edit_course_route(id):
    if request.method == "POST":
        name = request.form["name"]
        course_id = request.form["course_id"]
        teacher = request.form["teacher"]
        credits = request.form["credits"]
        old_course_id = request.form["course_id"]
        update_student(id, name, course_id, teacher, credits ,old_course_id)
        flash("Course edited with success!")
        return redirect(url_for("dashboard_courses"))

    else:
        course = get_course(id)
        return render_template("edit_course.html", course = course)
# ---------------------------
# Avvio con HTTPS in sviluppo
# ---------------------------
if __name__ == "__main__":
    # Devi generare prima i certificati self-signed:
    # openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
    app.run(ssl_context=(
        r"C:\Users\fabio\OneDrive\Desktop\student_project\cert.pem",
        r"C:\Users\fabio\OneDrive\Desktop\student_project\key.pem"
    ), debug=True)
