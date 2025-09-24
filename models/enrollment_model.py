# models/enrollment_model.py
from db import get_db_connection

def get_all_enrollments():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM enrollment")
    enrollments = cursor.fetchall()
    conn.close()
    return enrollments

def get_enrollment(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM enrollment WHERE id = %s",(id,))
    student = cursor.fetchone()
    conn.close()
    return student


def add_enroll(student_id, course_id, registration_date, mark, status):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO enrollment(student_id, course_id, registrazion_date, mark, status) VALUES (%s, %s, %s, %s, %s)",
        (student_id, course_id, registration_date, mark, status)
    )
    conn.commit()
    conn.close()


def delete_enroll(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM enrollment WHERE student_id = %s", (student_id,)
    )
    conn.commit()
    conn.close()


def update_enroll(id, student_id, course_id, registration_date, mark, status):
    conn = get_db_connection()
    cursor = conn.cursor()


    cursor.execute(
        """ UPDATE enrollment 
        SET student_id=%s, course_id=%s, registrazion_date=%s, mark=%s, status=%s 
        WHERE id=%s
    """, (student_id, course_id, registration_date, mark, status, id)
                   )

    conn.commit()
    conn.close()


def get_enrollment_from_course():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT c.code AS course_code,
               c.name AS course_name,
               COUNT(e.student_id) AS num_students
        FROM courses c
        LEFT JOIN enrollment e ON c.code = e.course_id
        GROUP BY c.code, c.name
        ORDER BY c.name ASC
    """)

    result = cursor.fetchall()
    cursor.close()
    conn.close()

    return result


def get_passed__not_from_course():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT c.code AS course_code,
               c.name AS course_name,
               SUM(CASE WHEN e.status = 'passed' THEN 1 ELSE 0 END) AS num_passed,
               SUM(CASE WHEN e.status = 'enrolled' THEN 1 ELSE 0 END) AS not_passed
        FROM courses c
        LEFT JOIN enrollment e ON c.code = e.course_id
        GROUP BY c.code, c.name
        ORDER BY c.name ASC
    """)



    result = cursor.fetchall()
    cursor.close()
    conn.close()

    return result





def get_marks_from_enrollments():
    conn = get_db_connection();
    cursor = conn.cursor();
    cursor.execute(
                """SELECT 
            e.course_id,
            e.mark,
            COUNT(*) AS num_passed
        FROM enrollment e
        WHERE e.status = 'passed'
        GROUP BY e.course_id, e.mark
        ORDER BY e.course_id, e.mark;
        """
    )
    result = cursor.fetchall()
    cursor.close()
    conn.close()

    return  result
