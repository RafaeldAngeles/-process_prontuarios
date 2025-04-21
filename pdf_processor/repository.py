import psycopg2
import os
from dotenv import load_dotenv
from .interfaces.i_repository import IRepository

class PostgreSQLRepository(IRepository):
    def __init__(self):
        load_dotenv()
        self.conn = psycopg2.connect(
            database=os.getenv("DATABASE_NAME"),
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
            host=os.getenv("DATABASE_HOST"),
            port=os.getenv("DATABASE_PORT")
        )

    def save(self, data: dict) -> None:
        with self.conn.cursor() as cursor:
            cursor.execute("""
    INSERT INTO user_data (
        full_name, birth_date, address, profession, phone,
        email, father_name, mother_name, main_complaint,
        father_age, mother_age
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data["full_name"], data["birth_date"], data["address"], data["profession"],
        data["phone"], data["email"], data["father_name"], data["mother_name"],
        data["main_complaint"], data["father_age"], data["mother_age"]
    ))
            self.conn.commit()

    def __del__(self):
        self.conn.close()
