import os
from dotenv import load_dotenv

load_dotenv("../.env")
#TEST
# print(f"ALIVE\npostgresql+pg8000://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/postgres\n\n")