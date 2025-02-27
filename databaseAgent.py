import google.generativeai as genai
from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
import psycopg2
import re
import pandas as pd
from tabulate import tabulate
from sqlalchemy import text  # ✅ Import text() for raw SQL execution

# ✅ Set up Gemini API Key
genai.configure(api_key="AIzaSyAwQ8kR0K4tHxAqfiPyP-NpkvZCHZCGBRs")

# ✅ Initialize the Gemini model
model = genai.GenerativeModel('gemini-pro')

# ✅ PostgreSQL Database Configuration
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "10.229.40.62"  # e.g., "localhost" or "your-db-host.com"
DB_PORT = "5432"  # Default PostgreSQL port
DB_NAME = "nmsdb"

# ✅ Construct the PostgreSQL URI
db_uri = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# ✅ Connect to the database
db = SQLDatabase.from_uri(db_uri)
query_tool = QuerySQLDataBaseTool(db=db)

def clean_sql_output(raw_sql):
    """
    Cleans Gemini's SQL output by removing markdown formatting and unnecessary text.
    """
    cleaned_sql = re.sub(r"```sql|```", "", raw_sql).strip()  # Remove triple backticks and 'sql'
    cleaned_sql = cleaned_sql.rstrip(";")  # ✅ Remove trailing semicolon (important)
    return cleaned_sql

def execute_query(sql_query):
    """
    Executes the SQL query and returns results in a tabular format.
    """
    try:
        with db._engine.connect() as connection:
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
print("Welcome to the Gemini SQL Agent! Type 'exit' to quit.")
while True:
    user_input = input("\nYou: ")

    # Exit Condition
    if user_input.lower() == 'exit':
        print("Goodbye!")
        break

    # Step 1️⃣: Convert Natural Language to SQL using Gemini
    prompt = f"Convert this into a PostgreSQL SQL query: {user_input}. Only return the SQL query without any explanations, markdown, or extra formatting."
    response = model.generate_content(prompt)
    
    sql_query = clean_sql_output(response.text)
    print("\n🔍 Generated SQL Query:", sql_query)

    # Step 2️⃣: Execute SQL Query and Display Result
    execute_query(sql_query)

