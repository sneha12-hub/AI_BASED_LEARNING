import requests
from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
import psycopg2
import re
import pandas as pd
from tabulate import tabulate
from sqlalchemy import create_engine, text  # ✅ Corrected import

# ✅ Ollama DeepSeek API URL
OLLAMA_URL = "http://10.229.43.133:11434/api/generate"

# ✅ PostgreSQL Database Configuration
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "10.229.40.62"  # e.g., "localhost" or "your-db-host.com"
DB_PORT = "5432"  # Default PostgreSQL port
DB_NAME = "nmsdb"

# ✅ Construct the PostgreSQL URI
db_uri = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# ✅ Create Database Engine
engine = create_engine(db_uri)

def clean_sql_output(raw_sql):
    """
    Cleans DeepSeek's SQL output by removing markdown formatting and unnecessary text.
    """
    cleaned_sql = re.sub(r"```sql|```", "", raw_sql).strip()  # Remove triple backticks and 'sql'
    cleaned_sql = cleaned_sql.rstrip(";")  # ✅ Remove trailing semicolon
    return cleaned_sql

def deepseek_generate_sql(natural_text):
    """
    Uses Ollama's DeepSeek model to generate SQL queries from natural language.
    """
    payload = {
        "model": "deepseek",  # Model name in Ollama
        "prompt": f"Convert this natural language request into a PostgreSQL SQL query: {natural_text}. Only return the SQL query, without explanations, markdown, or extra formatting.",
        "stream": False  # Get the full response at once
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        sql_query = response.json().get("response", "").strip()
        return clean_sql_output(sql_query)
    
    except requests.exceptions.RequestException as e:
        print("\n❌ Error: Failed to get SQL from DeepSeek:", e)
        return None

def execute_query(sql_query):
    """
    Executes the SQL query and returns results in a tabular format.
    """
    if not sql_query:
        print("\n❌ No SQL query generated.")
        return

    try:
        with engine.connect() as connection:
            # ✅ Use text() to execute raw SQL
            result = connection.execute(text(sql_query))
            rows = result.fetchall()
            columns = result.keys()  # Extract column names
        
        # Convert result to a DataFrame
        df = pd.DataFrame(rows, columns=columns)

        # Print result as a table
        if df.empty:
            print("\n🔍 No results found.")
        else:
            print("\n✅ Query Result:\n")
            print(tabulate(df, headers="keys", tablefmt="psql"))  # Pretty table format

    except Exception as e:
        print("\n❌ Error executing query:", e)

# ✅ Chatbot Loop
print("Welcome to the DeepSeek SQL Agent! Type 'exit' to quit.")
while True:
    user_input = input("\nYou: ")

    # Exit Condition
    if user_input.lower() == 'exit':
        print("Goodbye!")
        break

    # Step 1️⃣: Convert Natural Language to SQL using DeepSeek
    sql_query = deepseek_generate_sql(user_input)
    print("\n🔍 Generated SQL Query:", sql_query)

    # Step 2️⃣: Execute SQL Query and Display Result
    execute_query(sql_query)
