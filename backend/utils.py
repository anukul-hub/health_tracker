import openai
from sqlalchemy import text
from models.database import engine

# Configure OpenAI (replace YOUR_API_KEY with actual API key)
openai.api_key = "YOUR_API_KEY"

def generate_sql(prompt: str) -> str:
    """
    Generate an SQL query based on the natural language prompt.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"]

def execute_sql(sql: str):
    """
    Execute the provided SQL query on the database.
    """
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        return [dict(row) for row in result]
