from fastapi import FastAPI, Request
from sqlmodel import SQLModel, create_engine, text
from practica3.Repository import DirectoryRepository
from practica3.directoryDTO import DirectoryDTO
from dotenv import load_dotenv
import os

app = FastAPI()

load_dotenv("../.env")

#HACK: This checks if database exists and creates it if not, not very proud of how it's done but it works
init = create_engine(f"postgresql+pg8000://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/postgres", isolation_level="AUTOCOMMIT")

with init.connect() as connection:
  result = connection.execute(text(f"select exists(SELECT datname FROM pg_catalog.pg_database WHERE lower(datname) = lower('{os.getenv('DB_NAME')}'));"))
  if not result.fetchone().tuple()[0]:
    connection.execute(text(f"CREATE DATABASE {os.getenv('DB_NAME')};"))

init.dispose()

engine = create_engine(f"postgresql+pg8000://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME').lower()}")
SQLModel.metadata.create_all(engine)
directory_repo: DirectoryRepository = DirectoryRepository(engine)

@app.get("/status")
def get_status():
  return "Pong!"

@app.get("/directories")
def get_all_directories(request: Request, perpage : int | None=5, page: int | None= 1):
  urlobj = request.url
  url = str(urlobj)
  count = directory_repo.get_count()
  next = url.replace("&page="+str(page),"&page="+str(page+1))
  next = next.replace("?page="+str(page),"?page="+str(page+1))
  if((page)*perpage >= count):
    next = None
  prev = url.replace("&page="+str(page),"&page="+str(page-1))
  prev = prev.replace("?page="+str(page),"?page="+str(page-1))
  if(page == 1):
    prev = None
  result = { "count": count, "next":next, "previous":prev, "results":directory_repo.find_all(page, perpage)}
  return result

@app.get("/directories/{id}")
def get_directory_by_id(id: int):
  return directory_repo.find_by_id(id)

@app.post("/directories")
def create_directory(directory: DirectoryDTO):
  return directory_repo.create(directory.name, directory.emails)


@app.put("/directories/{id}")
def update_directory(id: int, directory: DirectoryDTO):
  return directory_repo.update(id, directory.name, directory.emails)

@app.patch("/directories/{id}")
def partially_update_directory(id: int, name: (str | None) = None, emails: (list[str] | None) = None):
  return directory_repo.update(id, name, emails)

@app.delete("/directories/{id}")
def delete_directory_by_id(id: int):
  return directory_repo.delete(id)
