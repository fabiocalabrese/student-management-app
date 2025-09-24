# models/student_model.py
from db import get_db_connection
from flask import request, redirect,render_template,url_for


def get_all_students():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM student")
    students = cursor.fetchall()
    conn.close()
    return students


def get_student(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM student WHERE id = %s",(id,))
    student = cursor.fetchone()
    conn.close()
    return student


def add_student(name, surname, email, born_date, student_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO student (name, surname, email, born_date, student_id) VALUES (%s, %s, %s, %s, %s)",
        (name, surname, email, born_date, student_id)
    )
    conn.commit()
    conn.close()


def delete_student(id_num,student_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM enrollment WHERE student_id = %s", (student_id,)
    )
    cursor.execute(
        "DELETE FROM student WHERE id = %s", (id_num,)
    )
    conn.commit()
    conn.close()


def update_student(id,name, surname, email, born_date, student_id, old_student_id):
    conn = get_db_connection()
    cursor = conn.cursor()


    cursor.execute(
        """ UPDATE student 
        SET name=%s, surname=%s, email=%s, born_date=%s, student_id=%s 
        WHERE id=%s
    """, (name, surname, email, born_date, student_id,id)
                   )

    if old_student_id != student_id:
        cursor.execute("""
               UPDATE enrollment 
               SET student_id = %s 
               WHERE student_id = %s
           """, (student_id, old_student_id))

    conn.commit()
    conn.close()