from pydantic import BaseModel
from mcp_server import mcp

class EmployeeRequest(BaseModel):
    employee_id: str

@mcp.tool(
    name="get_employee_metadata",
    description="Returns anonymized employee metadata"
)
def get_employee_metadata(req: EmployeeRequest):
    # Mock DB result (PII REMOVED)
    return {
        "role": "Senior Engineer",
        "experience_years": 8,
        "performance": "High",
        "skills": ["Python", "Spark", "System Design"]
    }

class GrowthRequest(BaseModel):
    role: str
    experience_years: int
    performance: str

@mcp.tool(
    name="explain_employee_growth",
    description="Explains career growth based on role & experience"
)
def explain_employee_growth(req: GrowthRequest):
    return {
        "summary": f"{req.role} shows strong growth potential.",
        "recommendations": [
            "Own architecture decisions",
            "Mentor junior engineers",
            "Lead cross-team initiatives"
        ]
    }