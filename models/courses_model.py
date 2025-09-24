# models/course_model.py
from db import get_db_connection

def get_all_courses():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    conn.close()
    return courses


def get_course(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM courses WHERE id = %s",(id,))
    course = cursor.fetchone()
    conn.close()
    return course


def add_course(name, course_id, teacher, credits):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO courses (name, code, teacher, credits ) VALUES (%s, %s, %s, %s)",
        (name, course_id, teacher, credits)
    )
    conn.commit()
    conn.close()


def delete_course(id,course_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM enrollment WHERE course_id = %s", (course_id,)
    )
    cursor.execute(
        cursor.execute("DELETE FROM courses WHERE id = %s", (id,))
    )
    conn.commit()
    conn.close()


def update_course(id, name, course_id, teacher, credits, old_course_id):
    conn = get_db_connection()
    cursor = conn.cursor()


    cursor.execute(
        """ UPDATE courses
        SET name=%s, code=%s, teacher=%s, credits=%s
        WHERE id=%s
    """, (name, course_id, teacher, credits, id)
                   )

    if old_course_id != course_id:
        cursor.execute("""
               UPDATE enrollment 
               SET course_id = %s 
               WHERE course_id = %s
           """, (course_id, old_course_id))

    conn.commit()
    conn.close()