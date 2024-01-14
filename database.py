from flask import jsonify, url_for
import pymysql
import os

from dotenv import load_dotenv
if not os.getenv("DB_HOST"):
    load_dotenv()

def connect_to_database():
    host = os.environ.get("DB_HOST")
    user = os.environ.get("DB_USER")
    password = os.environ.get("DB_PASSWORD")
    database = os.environ.get("DB_NAME")

    try:
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=3306,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit = True,
            ssl      = {
                "ca": "/etc/ssl/cert.pem"
            }
        )

        print("Connected to the database!")

        return connection

    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def close_connection(connection):
    if connection:
        connection.close()
        print("Connection closed.")

def retrieve_jobs_data(connection):
    try:
        with connection.cursor() as cursor:
            sql_query = "SELECT * FROM jobs"
            
            cursor.execute(sql_query)
            
            result = cursor.fetchall()

            rows_as_dicts = []
            for row in result:
                row_dict = dict(row)
                rows_as_dicts.append(row_dict)

            return rows_as_dicts
                
    except Exception as e:
        print(f"Error retrieving data: {e}")

def load_jobs_from_db():
    connection = connect_to_database()
    if connection:
        jobs_data = retrieve_jobs_data(connection)
        jobs = []
        for job in jobs_data:
            jobs.append(job)
        close_connection(connection)
        return jobs

def insert_job_to_db(title, location, description, salary, currency):
    connection = connect_to_database()

    if not connection:
        return jsonify({'success': False, 'message': 'Unable to connect to the database'})

    try:
        with connection.cursor() as cursor:
            sql_query = "INSERT INTO jobs (title, location, description, salary, currency) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql_query, (title, location, description, salary or None, currency or None))
        return jsonify({'success': True, 'message': 'Job posted successfully'})
        

    except Exception as e:
        return jsonify({'success': False, 'message': f'Error posting job: {e}'})

    finally:
        close_connection(connection)