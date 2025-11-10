import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        return connection
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None


def get_engine():
    try:
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        host = os.getenv("DB_HOST")
        database = os.getenv("DB_NAME")
        engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")
        return engine
    except Exception as e:
        print(f"Error creating SQLAlchemy engine: {e}")
        return None