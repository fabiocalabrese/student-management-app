import mysql.connector

def get_db_connection(user=None, password=None):
    if not user or not password:
        from flask import session
        user = session.get("username")
        password = session.get("password")

    conn = mysql.connector.connect(
        host="localhost",
        user=user,
        password=password,
        database="student_project"
    )
    return conn