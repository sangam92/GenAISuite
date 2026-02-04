import os
from dotenv import load_dotenv
import psycopg2

def fetch_employee_info(emp_id: str):
    try:
        load_dotenv()

        conn = psycopg2.connect(
            host=os.getenv("PG_HOST"),
            port=os.getenv("PG_PORT"),
            database=os.getenv("PG_DATABASE"),
            user=os.getenv("PG_USER"),
            password=os.getenv("PG_PASSWORD"),
            connect_timeout=os.getenv("PG_CONNECT_TIMEOUT")
        )
        print(conn)
        print("Connected successfully!")

        cur = conn.cursor()  # create cursor

        cur.execute("""
            SELECT employee_id, designation, salary, "Aspiration"
            FROM public."Employee"
            WHERE employee_id = %s
        """, (emp_id,))

        row = cur.fetchone()  # fetch result from cursor

        cur.close()
        conn.close()

        if not row:
            return f"No employee found with ID {emp_id}"

        return {
            "employee_id": row[0],
            "designation": row[1],
            "salary": row[2],
            "future_aspiration": row[3]
        }

    except Exception as e:
        return f"Database error: {str(e)}"
