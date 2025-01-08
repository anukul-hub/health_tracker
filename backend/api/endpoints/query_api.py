import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import asyncpg
import requests
import os
from dotenv import load_dotenv
import google.generativeai as genai
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Load environment variables from .env file
load_dotenv(dotenv_path='G:/health_fitness_tracker/frontend/.env')
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Input model for SQL-based queries
class SQLQueryRequest(BaseModel):
    question: str


async def get_database_schema():
    """
    Endpoint to fetch the structure of all tables in the PostgreSQL database.
    Returns table names and their columns.
    """
    try:
        conn = await asyncpg.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        
        tables = await conn.fetch(""" 
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public';
        """)

        table_structure = []
        for table in tables:
            table_name = table['table_name']
            columns = await conn.fetch(f"""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = '{table_name}';
            """)
            column_names = [column['column_name'] for column in columns]
            table_structure.append({
                "name": table_name,
                "columns": column_names
            })

        await conn.close()
        return table_structure
    except Exception as e:
        logger.error(f"Error fetching table structure: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching table structure: {str(e)}")


async def generate_sql_from_gemini(question: str) -> str:
    """
    Generate an SQL query using Gemini API.
    """
    logger.info("Generating SQL from Gemini API...")
    schema = await get_database_schema()

    schema_text = "\n".join([f"Table {table['name']}: {', '.join(table['columns'])}" for table in schema])
    logger.info("Schema text prepared for Gemini API: %s", schema_text)

    prompt = (
        f"Here is the schema of the database:\n{schema_text}\n\n"
        f"User question: {question}\n\n"
        "Please generate an SQL query based on the above schema and user question."
    )

    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        
        sql_query = response.text.strip()
        logger.info("Generated SQL query: %s", sql_query)
        
        # Clean up the query by removing the markdown code block
        if sql_query.startswith("```sql") and sql_query.endswith("```"):
            sql_query = sql_query[7:-3].strip()  # Remove the ```sql and ending ```

        # Basic validation: Ensure the query starts with SELECT
        if not sql_query.lower().startswith("select"):
            logger.warning(f"Generated query is not a valid SQL SELECT: {sql_query}")
        
        return sql_query
    except Exception as e:
        logger.exception("Error generating SQL from Gemini: %s", e)
        return f"Failed to generate a valid SQL query: {str(e)}"


async def execute_sql(sql_query: str):
    """
    Function to execute SQL query on the PostgreSQL database and return the results.
    """
    logger.info("Executing SQL query: %s", sql_query)
    try:
        conn = await asyncpg.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        result = await conn.fetch(sql_query)
        await conn.close()
        logger.info("SQL query executed successfully. Result: %s", result)
        return result
    except Exception as e:
        logger.error("Error executing SQL query: %s", e)
        raise Exception(f"Error executing SQL query: {str(e)}")


@router.post("/ask")
async def ask_question(request: SQLQueryRequest):
    """
    Endpoint to process a user's question, generate an SQL query,
    and return the results.
    """
    logger.info("Received question: %s", request.question)
    try:
        sql_query = await generate_sql_from_gemini(request.question)
        logger.info("Generated SQL query: %s", sql_query)
        result = await execute_sql(sql_query)
        logger.info("Final result returned to client: %s", result)
        return {"query": sql_query, "result": result}
    except requests.RequestException as e:
        logger.error("Error communicating with Gemini API: %s", e)
        raise HTTPException(status_code=500, detail=f"Error communicating with Gemini API: {str(e)}")
    except Exception as e:
        logger.error("Error in ask_question: %s", e)
        raise HTTPException(status_code=500, detail=str(e))








# import logging
# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# import asyncpg
# import requests
# import os
# from dotenv import load_dotenv
# import google.generativeai as genai
# import asyncio

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# router = APIRouter()

# # Load environment variables from .env file
# load_dotenv(dotenv_path='G:/health_fitness_tracker/frontend/.env')
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# # Input model for SQL-based queries
# class SQLQueryRequest(BaseModel):
#     question: str


# async def get_database_schema():
#     """
#     Endpoint to fetch the structure of all tables in the PostgreSQL database.
#     Returns table names and their columns.
#     """
#     try:
#         conn = await asyncpg.connect(
#             user=os.getenv("DB_USER"),
#             password=os.getenv("DB_PASSWORD"),
#             database=os.getenv("DB_NAME"),
#             host=os.getenv("DB_HOST"),
#             port=os.getenv("DB_PORT")
#         )
        
#         tables = await conn.fetch("""
#             SELECT table_name 
#             FROM information_schema.tables 
#             WHERE table_schema = 'public';
#         """)

#         table_structure = []
#         for table in tables:
#             table_name = table['table_name']
#             columns = await conn.fetch(f"""
#                 SELECT column_name 
#                 FROM information_schema.columns 
#                 WHERE table_name = '{table_name}';
#             """)
#             column_names = [column['column_name'] for column in columns]
#             table_structure.append({
#                 "name": table_name,
#                 "columns": column_names
#             })

#         await conn.close()
#         return table_structure
#     except Exception as e:
#         logger.error(f"Error fetching table structure: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Error fetching table structure: {str(e)}")


# async def generate_sql_from_gemini(question: str) -> str:
#     """
#     Generate an SQL query using Gemini API.
#     """
#     logger.info("Generating SQL from Gemini API...")
#     schema = await get_database_schema()

#     schema_text = "\n".join([f"Table {table['name']}: {', '.join(table['columns'])}" for table in schema])
#     logger.info("Schema text prepared for Gemini API: %s", schema_text)

#     prompt = (
#         f"Here is the schema of the database:\n{schema_text}\n\n"
#         f"User question: {question}\n\n"
#         "Please generate an SQL query based on the above schema and user question."
#     )

#     try:
#         genai.configure(api_key=GEMINI_API_KEY)
#         model = genai.GenerativeModel("gemini-1.5-flash")
#         response = model.generate_content(prompt)
        
#         sql_query = response.text.strip()
#         logger.info("Generated SQL query: %s", sql_query)
        
#         # Log a warning instead of raising an exception if the query is not valid
#         if not sql_query.lower().startswith("select"):
#             logger.warning(f"Generated query is not a valid SQL SELECT: {sql_query}")
        
#         return sql_query
#     except Exception as e:
#         logger.exception("Error generating SQL from Gemini: %s", e)
#         return f"Failed to generate a valid SQL query: {str(e)}"


# # async def execute_sql(sql_query: str):
# #     """
# #     Function to execute SQL query on the PostgreSQL database and return the results.
# #     """
# #     logger.info("Executing SQL query: %s", sql_query)
# #     try:
# #         conn = await asyncpg.connect(
# #             user=os.getenv("DB_USER"),
# #             password=os.getenv("DB_PASSWORD"),
# #             database=os.getenv("DB_NAME"),
# #             host=os.getenv("DB_HOST"),
# #             port=os.getenv("DB_PORT")
# #         )
# #         result = await conn.fetch(sql_query)
# #         await conn.close()
# #         logger.info("SQL query executed successfully. Result: %s", result)
# #         return result
# #     except Exception as e:
# #         logger.error("Error executing SQL query: %s", e)
# #         raise Exception(f"Error executing SQL query: {str(e)}")


# @router.post("/ask")
# async def ask_question(request: SQLQueryRequest):
#     """
#     Endpoint to process a user's question, generate an SQL query,
#     and return the results.
#     """
#     logger.info("Received question: %s", request.question)
#     try:
#         sql_query = await generate_sql_from_gemini(request.question)
#         logger.info("Generated SQL query: %s", sql_query)
#         # result = await execute_sql(sql_query)
#         # logger.info("Final result returned to client: %s", result)
#         return {"query": sql_query}
#     except requests.RequestException as e:
#         logger.error("Error communicating with Gemini API: %s", e)
#         raise HTTPException(status_code=500, detail=f"Error communicating with Gemini API: {str(e)}")
#     except Exception as e:
#         logger.error("Error in ask_question: %s", e)
#         raise HTTPException(status_code=500, detail=str(e))
    





















# import logging
# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# import psycopg2
# import requests
# import os
# from dotenv import load_dotenv
# import google.generativeai as genai

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# router = APIRouter()

# # Load environment variables from .env file
# load_dotenv(dotenv_path='G:/health_fitness_tracker/frontend/.env')
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# # Input model for SQL-based queries
# class SQLQueryRequest(BaseModel):
#     question: str


# def get_database_schema():
#     """
#     Endpoint to fetch the structure of all tables in the PostgreSQL database.
#     Returns table names and their columns.
#     """
#     try:
#         conn = psycopg2.connect(
#             dbname=os.getenv("DB_NAME"),
#             user=os.getenv("DB_USER"),
#             password=os.getenv("DB_PASSWORD"),
#             host=os.getenv("DB_HOST"),
#             port=os.getenv("DB_PORT")
#         )
#         cursor = conn.cursor()

#         cursor.execute("""
#             SELECT table_name 
#             FROM information_schema.tables 
#             WHERE table_schema = 'public';
#         """)
#         tables = cursor.fetchall()

#         table_structure = []
#         for table_name in tables:
#             table_name = table_name[0]
#             cursor.execute(f"""
#                 SELECT column_name 
#                 FROM information_schema.columns 
#                 WHERE table_name = '{table_name}';
#             """)
#             columns = cursor.fetchall()
#             column_names = [column[0] for column in columns]
#             table_structure.append({
#                 "name": table_name,
#                 "columns": column_names
#             })

#         return table_structure
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error fetching table structure: {str(e)}")
#     finally:
#         if conn:
#             conn.close()

# def generate_sql_from_gemini(question: str) -> str:
#     """
#     Generate an SQL query using Gemini API.
#     """
#     logger.info("Generating SQL from Gemini API...")
#     schema = get_database_schema()

#     schema_text = "\n".join([f"Table {table['name']}: {', '.join(table['columns'])}" for table in schema])
#     logger.info("Schema text prepared for Gemini API: %s", schema_text)

#     prompt = (
#         f"Here is the schema of the database:\n{schema_text}\n\n"
#         f"User question: {question}\n\n"
#         "Please generate an SQL query based on the above schema and user question."
#     )

#     try:
#         genai.configure(api_key=GEMINI_API_KEY)
#         model = genai.GenerativeModel("gemini-1.5-flash")
#         response = model.generate_content(prompt)
        
#         sql_query = response.text.strip()
#         logger.info("Generated SQL query: %s", sql_query)
        
#         # Basic validation
#         if not sql_query.lower().startswith("select"):
#             raise Exception(f"Invalid SQL query generated: {sql_query}")
        
#         return sql_query
#     except Exception as e:
#         logger.exception("Error generating SQL from Gemini: %s", e)
#         raise Exception("Failed to generate a valid SQL query.")

# # def generate_sql_from_gemini() -> str:
# #     """
# #     Generate an SQL query using Gemini API for testing.
# #     """
# #     question = "What is the total sales by product category?"

# #     logger.info("Generating response from Gemini API...")

# #     prompt = (
# #         f"User question: {question}\n\n"
# #         "Please provide a response in text format based on the user's question."
# #     )

# #     try:
# #         genai.configure(api_key=GEMINI_API_KEY)
# #         model = genai.GenerativeModel("gemini-1.5-flash")
# #         response = model.generate_content(prompt)
        
# #         generated_response = response.text.strip()
# #         logger.info("Generated response: %s", generated_response)
        
# #         return generated_response
# #     except Exception as e:
# #         logger.exception("Error generating response from Gemini: %s", e)
# #         raise Exception("Failed to generate a valid response.")



# def execute_sql(sql_query: str):
#     """
#     Function to execute SQL query on the PostgreSQL database and return the results.
#     """
#     logger.info("Executing SQL query: %s", sql_query)
#     try:
#         conn = psycopg2.connect(
#             dbname=os.getenv("DB_NAME"),
#             user=os.getenv("DB_USER"),
#             password=os.getenv("DB_PASSWORD"),
#             host=os.getenv("DB_HOST"),
#             port=os.getenv("DB_PORT")
#         )
#         cursor = conn.cursor()
#         cursor.execute(sql_query)
#         result = cursor.fetchall()
#         conn.commit()
#         logger.info("SQL query executed successfully. Result: %s", result)
#         return result
#     except Exception as e:
#         logger.error("Error executing SQL query: %s", e)
#         raise Exception(f"Error executing SQL query: {str(e)}")
#     finally:
#         if conn:
#             conn.close()
#             logger.info("Database connection closed.")

# @router.post("/ask")
# async def ask_question(request: SQLQueryRequest):
#     """
#     Endpoint to process a user's question, generate an SQL query,
#     and return the results.
#     """
#     logger.info("Received question: %s", request.question)
#     try:
#         sql_query = generate_sql_from_gemini(request.question)
#         logger.info("Generated SQL query: %s", sql_query)
#         result = execute_sql(sql_query)
#         logger.info("Final result returned to client: %s", result)
#         return {"query": sql_query, "result": result}
#     except requests.RequestException as e:
#         logger.error("Error communicating with Gemini API: %s", e)
#         raise HTTPException(status_code=500, detail=f"Error communicating with Gemini API: {str(e)}")
#     except Exception as e:
#         logger.error("Error in ask_question: %s", e)
#         raise HTTPException(status_code=500, detail=str(e))




