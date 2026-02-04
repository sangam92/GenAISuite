import os
from langchain_google_genai import ChatGoogleGenerativeAI
from fastapi import FastAPI
from pydantic import BaseModel
from db_conn import fetch_employee_info
import app as app_config  # avoid name clash


# 1. Set up your API Key
if not getattr(app_config, "API_KEY", None):
    raise RuntimeError("API_KEY not found. Put it in `app.env` or set the `API_KEY` environment variable.")

os.environ["GOOGLE_API_KEY"] = app_config.API_KEY


# 2. Initialize FastAPI app
api = FastAPI(title="Employee Insight Agent API")


# 3. Initialize Gemini (LangChain wrapper)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
    max_retries=2,
)


# 4. Keep your agent function unchanged except return fix
def employee_agent(question: str, emp_id: str):
    """AI Agent that fetches DB data and explains it"""

    db_result = fetch_employee_info(emp_id)

    if not db_result:
        return f"No employee found with ID {emp_id}"

    prompt = f"""
    You are an AI assistant and data interpreter.
    Use the database result below to answer the question in a professional, structured, and human-friendly explanation.

    Question: {question}

    Database Result:
    {db_result}

    Instructions:
    - Explain designation and salary context
    - Provide career path insight based on aspiration
    - Keep tone suitable for engineering/data leadership roles
    - If salary looks low/high, explain market relativity
    - Add future growth suggestions
    """

    response = llm.invoke(prompt)
    return response.content  # LangChain models return .content


# 5. Request body schema for UI/API calls
class EmployeeQuery(BaseModel):
    employee_id: int
    question: str


# 6. API endpoint using your current code
@api.post("/employee/explain")
def explain_employee(q: EmployeeQuery):
    explanation = employee_agent(q.question, str(q.employee_id))
    return {"explanation": explanation}

"""
# 7. Optional local test
if __name__ == "__main__":
    print(employee_agent(
        question="Explain this employee's profile and future growth",
        emp_id="101"
    ))
"""