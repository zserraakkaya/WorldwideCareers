import pymysql
import os

from dotenv import load_dotenv
load_dotenv()

def connect_to_database():
    host = os.getenv("DB_HOST")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    database = os.getenv("DB_NAME")

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