import os
from dotenv import load_dotenv

load_dotenv()


api_key = os.environ.get("API_KEY")
database = os.environ.get("DATABASE_NAME", "default.db")

print(f"Using database: {database} ")
