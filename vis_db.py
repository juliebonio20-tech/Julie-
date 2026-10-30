# ===== DILI PWEDI PALITAN ANG PANGALAN SA FILE NGA NI =====
# Kini nga file (vis_db.py) gi-import sa main_visitor.py ug vis_ops.py
# Kung i-rename nimo ni, palitan usab nimo ang "import vis_db" sa maong duha ka files
import os

import mysql.connector
from mysql.connector import Error


DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "visitor_log_db")


def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4",
        use_pure=True,
    )


def test_connection():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT 1 FROM visitor_log LIMIT 1")
            cursor.fetchone()
            return True, "Koneksyon sa Visitor Log database ay OK na."
        return False, "Hindi makakonekta sa database."
    except Error as error:
        return False, str(error)
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def next_vno():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT visitor_no FROM visitor_log ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        if not result:
            return "V-0001"
        last_no = result[0]
        try:
            num = int(last_no.split("-")[1]) + 1
            return f"V-{num:04d}"
        except (IndexError, ValueError):
            return "V-0001"
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def sign_in(record):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO visitor_log
                (visitor_no, full_name, company_office, id_type, id_no, purpose,
                 person_to_visit, contact_no, time_in, time_out, guard_on_duty, remarks, status)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                record["visitor_no"],
                record["full_name"],
                record["company_office"],
                record["id_type"],
                record["id_no"],
                record["purpose"],
                record["person_to_visit"],
                record["contact_no"],
                record["time_in"],
                record["time_out"],
                record["guard_on_duty"],
                record["remarks"],
                record["status"],
            ),
        )
        connection.commit()
        return cursor.lastrowid
    except Error:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def list_all():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM visitor_log ORDER BY id DESC")
        return cursor.fetchall()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def find_visitor(visitor_no):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM visitor_log WHERE visitor_no = %s", (visitor_no,))
        return cursor.fetchone()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def sign_out(visitor_no, time_out):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            UPDATE visitor_log
            SET time_out = %s, status = 'Umalis na'
            WHERE visitor_no = %s AND status = 'Nasa Loob'
            """,
            (time_out, visitor_no),
        )
        connection.commit()
        return cursor.rowcount > 0
    except Error:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def delete_visitor(visitor_no):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM visitor_log WHERE visitor_no = %s", (visitor_no,))
        connection.commit()
        return cursor.rowcount > 0
    except Error:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def clear_log():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM visitor_log")
        connection.commit()
        return cursor.rowcount
    except Error:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()
