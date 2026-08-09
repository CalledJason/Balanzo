import os

import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def test_connection():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not configured")

    with psycopg.connect(DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version()")
            result = cursor.fetchone()

            print("Connected to PostgreSQL")
            print(result[0])


if __name__ == "__main__":
    test_connection()