from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine, text
from Repository import DirectoryRepository
from directoryDTO import DirectoryDTO
from dotenv import load_dotenv
import os

app = FastAPI()

load_dotenv(".env")

#HACK: This checks if database exists and creates it if not, not very proud of how it's done but it works
init = create_engine(f"postgresql+pg8000://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/postgres", isolation_level="AUTOCOMMIT")

with init.connect() as connection:
  result = connection.execute(text(f"select exists(SELECT datname FROM pg_catalog.pg_database WHERE lower(datname) = lower('{os.getenv('DB_NAME')}'));"))
  if not result.fetchone().tuple()[0]:
    connection.execute(text(f"CREATE DATABASE {os.getenv('DB_NAME')};"))

init.dispose()

engine = create_engine(f"postgresql+pg8000://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")
SQLModel.metadata.create_all(engine)
directory_repo: DirectoryRepository = DirectoryRepository(engine)

@app.get("/status")
def get_status():
  return "Pong!"

@app.get("/directories")
def get_all_directories():
  return "Not Implemented"

@app.get("/directories/{id}")
def get_directory_by_id(id: int):
  return "Not Implemented"

@app.post("/directories")
def create_directory(directory: DirectoryDTO):
  return directory_repo.create(directory.name, directory.emails)


@app.put("/directories/{id}")
def update_directory(id: int, name: str, emails: list[str]):
  return "Not Implemented"

@app.patch("/directories/{id}")
def partially_update_directory(id: int, name: (str | None) = None, emails: (list[str] | None) = None):
  return "Not Implemented"

@app.delete("/directories/{id}")
def delete_directory_by_id(id: int):
  return "Not Implemented"
