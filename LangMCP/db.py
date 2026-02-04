from sqlalchemy import create_engine,text

DATABASE_URL = (
    "postgresql+psycopg2://postgres:postgres@localhost:5432/public"
)
engine = create_engine(DATABASE_URL)


def fetch_data(emp_id):
    query="""
        SELECT *
        FROM employees
            WHERE employee_id = :emp_id
    """


    with engine.connect() as conn:
        result = conn.execute(query,{"employee_id":emp_id}).fetchall()
        return result