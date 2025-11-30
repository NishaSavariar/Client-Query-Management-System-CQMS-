import mysql.connector
from datetime import datetime
import pandas as pd

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Iniya@08",
        database="cqms_simple",
        autocommit=True
    )

def insert_query(mail_id, mobile, heading, description):
    conn = get_db_connection()
    cursor = conn.cursor()

    created_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        """INSERT INTO queries 
           (mail_id, mobile_number, query_heading, query_description, status, query_created_time)
           VALUES (%s, %s, %s, %s, %s, %s)""",
        (mail_id, mobile, heading, description, "Open", created_time)
    )

    conn.commit()
    cursor.close()
    conn.close()

def get_all_queries(status_filter):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if status_filter == "All":
        cursor.execute("SELECT * FROM queries ORDER BY query_id DESC")
    else:
        cursor.execute(
            "SELECT * FROM queries WHERE status=%s ORDER BY query_id DESC",
            (status_filter,)
        )

    data = cursor.fetchall()

    cursor.close()
    conn.close()
    return data


def close_query_response(query_id, response):
    conn = get_db_connection()
    cursor = conn.cursor()

    closed_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        "UPDATE queries SET status='Closed', query_response=%s, query_closed_time=%s WHERE query_id=%s",
        (response, closed_time, query_id)
    )

    conn.commit()
    cursor.close()
    conn.close()

def load_all_queries_df():
    conn = get_db_connection()
    df = pd.read_sql("SELECT * FROM queries", conn)
    conn.close()
    return df

