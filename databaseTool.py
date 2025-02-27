from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
import os

# PostgreSQL Database Connection URI (Update these details)
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "10.229.40.62"  # e.g., "localhost" or "your-db-host.com"
DB_PORT = "5432"  # Default PostgreSQL port
DB_NAME = "nmsdb"

# Construct the PostgreSQL URI
db_uri = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Initialize the SQLDatabase instance
db = SQLDatabase.from_uri(db_uri)

# Initialize the QuerySQLDataBaseTool
query_tool = QuerySQLDataBaseTool(db=db)

# Example Query: Fetch all records from a specific table (Update table name)
query = "SELECT * FROM your_table LIMIT 10;"  # Modify the query as needed
result = query_tool.run(query)

# Print the query result
print("Query Result:", result)
