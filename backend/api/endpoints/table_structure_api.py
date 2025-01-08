
from fastapi import APIRouter, HTTPException
import psycopg2
from dotenv import load_dotenv
import os

router = APIRouter()

# Load environment variables from .env file
load_dotenv(dotenv_path='G:/health_fitness_tracker/frontend/.env')

@router.get("/table-structure")
async def get_table_structure():
    """
    Endpoint to fetch the structure of all tables in the PostgreSQL database.
    Returns table names and their columns.
    """
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        cursor = conn.cursor()

        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public';
        """)
        tables = cursor.fetchall()

        table_structure = []
        for table_name in tables:
            table_name = table_name[0]
            cursor.execute(f"""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = '{table_name}';
            """)
            columns = cursor.fetchall()
            column_names = [column[0] for column in columns]
            table_structure.append({
                "name": table_name,
                "columns": column_names
            })

        return table_structure
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching table structure: {str(e)}")
    finally:
        if conn:
            conn.close()

