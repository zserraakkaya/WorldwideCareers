from flask import jsonify, url_for
import pymysql
import os

from dotenv import load_dotenv
if not os.getenv("DB_HOST"):
    load_dotenv()

# initial connection to database
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

# close connection to database
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

# load all jobs for home.html
def load_jobs_from_db():
    connection = connect_to_database()
    if connection:
        jobs_data = retrieve_jobs_data(connection)
        jobs = []
        for job in jobs_data:
            jobs.append(job)
        close_connection(connection)
        return jobs

# when "post job" button clicked on post-job.html:
def insert_job_to_db(title, location, description, salary, currency, email):
    connection = connect_to_database()

    if not connection:
        return jsonify({'success': False, 'message': 'Unable to connect to the database'})

    try:
        with connection.cursor() as cursor:
            sql_query = "INSERT INTO jobs (title, location, description, salary, currency, email) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql_query, (title, location, description, salary or None, currency or None, email))
        return jsonify({'success': True, 'message': 'Job posted successfully'})
        

    except Exception as e:
        return jsonify({'success': False, 'message': f'Error posting job: {e}'})

    finally:
        close_connection(connection)

# when "see job details" button clicked on home.html:
def load_job_from_db(job_id):
    connection = connect_to_database()

    try:
        with connection.cursor() as cursor:
            sql_query = 'SELECT * FROM jobs WHERE id=%s'
            
            cursor.execute(sql_query, (job_id,))
            
            result = cursor.fetchone()  # Use fetchone() to get a single row

            if result:
                return dict(result)
            else:
                return None
                
    except Exception as e:
        print(f"Error retrieving data: {e}")

    finally:
        close_connection(connection)

# when "apply job" button clicked on apply-job.html:
def insert_job_application_to_db(first_name, last_name, date_of_birth, email):
    connection = connect_to_database()

    if not connection:
        return jsonify({'success': False, 'message': 'Unable to connect to the database'})

    try:
        with connection.cursor() as cursor:
            sql_query = "INSERT INTO job_applications (first_name, last_name, date_of_birth, email) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql_query, (first_name, last_name, date_of_birth, email))
        return jsonify({'success': True, 'message': 'Applied for job successfully'})
        

    except Exception as e:
        return jsonify({'success': False, 'message': f'Error applying job: {e}'})

    finally:
        close_connection(connection)