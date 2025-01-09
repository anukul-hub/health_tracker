from fastapi import APIRouter, HTTPException
import asyncpg
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
        # Connect to the PostgreSQL database asynchronously
        conn = await asyncpg.connect(
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )

        # Fetch all table names
        tables = await conn.fetch("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public';
        """)

        # Fetch column details for each table
        table_structure = []
        for table in tables:
            table_name = table["table_name"]
            columns = await conn.fetch(f"""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = $1;
            """, table_name)
            column_names = [column["column_name"] for column in columns]
            table_structure.append({
                "name": table_name,
                "columns": column_names
            })

        return table_structure
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching table structure: {str(e)}")
    finally:
        if conn:
            await conn.close()
