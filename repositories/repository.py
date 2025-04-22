from models.user import User
from typing import List, Optional
from dotenv import load_dotenv
import psycopg2
import os

class PostgreSQLRepository:
    def __init__(self):
        load_dotenv()
        self.conn = psycopg2.connect(
            database=os.getenv("DATABASE_NAME"),
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
            host=os.getenv("DATABASE_HOST"),
            port=os.getenv("DATABASE_PORT")
        )

    def get_all(self) -> List[User]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM user_data") 
        rows = cursor.fetchall()
        return [User(**dict(zip([desc[0] for desc in cursor.description], row))) for row in rows]

    def get_by_id(self, user_id: int) -> Optional[User]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM user_data WHERE id = %s", (user_id,))
        row = cursor.fetchone()
        if row:
            return User(**dict(zip([desc[0] for desc in cursor.description], row)))
        return None

    def update(self, user_id: int, data: dict):
        keys = ", ".join([f"{k} = %s" for k in data.keys()])
        values = list(data.values()) + [user_id]
        cursor = self.conn.cursor()
        cursor.execute(f"UPDATE user_data SET {keys} WHERE id = %s", values)
        self.conn.commit()

    def delete(self, user_id: int):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM user_data WHERE id = %s", (user_id,))
        self.conn.commit()

