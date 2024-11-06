from fastapi import FastAPI, Request, HTTPException
from sqlmodel import SQLModel, create_engine, text
from src.Repository import DirectoryRepository
from src.directoryDTO import DirectoryDTO
import os
import time

app = FastAPI()

#Keep retrying until DB connects
success = False
retry_count = 0
init = None
while (not success):
  try:
    init = create_engine(f"postgresql+pg8000://{os.getenv('DB_USERNAME', 'postgres')}:{os.getenv('DB_PASSWORD', 'grupo4')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '5432')}/postgres", isolation_level="AUTOCOMMIT")
    with init.connect() as connection:
      print("\033[92m" + "INFO" + "\033[0m" +":\tConnection success!")
      success = True
  except Exception as error:
    print("\033[91m" + "ERROR" + "\033[0m" +":\tConnection failed. Detail:\n",f"{error}")
    time.sleep(3)
    print("\033[92m" + "INFO" + "\033[0m" + f":\tNow retrying... ({retry_count})")
    retry_count += 1

#HACK: This checks if database exists and creates it if not, not very proud of how it's done but it works
with init.connect() as connection:
  db_name = os.getenv('DB_NAME', 'LosVinos').lower()
  result = connection.execute(text(f"select exists(SELECT datname FROM pg_catalog.pg_database WHERE lower(datname) = lower('{os.getenv('DB_NAME')}'));"))
  if not result.fetchone().tuple()[0]:
    connection.execute(text(f"CREATE DATABASE {db_name};"))

init.dispose()
engine = create_engine(f"postgresql+pg8000://{os.getenv('DB_USERNAME', 'postgres')}:{os.getenv('DB_PASSWORD', 'grupo4')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '5432')}/{db_name}")
SQLModel.metadata.create_all(engine)
directory_repo: DirectoryRepository = DirectoryRepository(engine)

@app.get("/status", status_code = 200)
def get_status():
  return "Pong!"

@app.get("/directories", status_code = 200)
def get_all_directories(request: Request, perpage : int | None=5, page: int | None= 1):
  #Construct next/prev url links
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
  
  #Obtain paginated result
  queryResult = directory_repo.find_all(page, perpage)
  if (queryResult == []):
    raise HTTPException(404, "No results found")
  result = { "count": count, "next":next, "previous":prev, "results":queryResult}
  return result

@app.get("/directories/{id}", status_code = 200)
def get_directory_by_id(id: int):
  result = directory_repo.find_by_id(id)
  if (result is None):
    raise HTTPException(404, "User not found")
  return result

@app.post("/directories", status_code = 201)
def create_directory(directory: DirectoryDTO):
  return directory_repo.create(directory.name, directory.emails)


@app.put("/directories/{id}", status_code=200)
def update_directory(id: int, directory: DirectoryDTO):
  result = directory_repo.update(id, directory.name, directory.emails)
  if (result is None):
    raise HTTPException(404, "Target user not found")
  return result

@app.patch("/directories/{id}", status_code=200)
def partially_update_directory(id: int, name: (str | None) = None, emails: (list[str] | None) = None):
  result = directory_repo.update(id, name, emails)
  if (result is None):
    raise HTTPException(404, "Target user not found")
  return result

@app.delete("/directories/{id}", status_code = 204)
def delete_directory_by_id(id: int):
  statusResult = directory_repo.delete(id)
  if (not statusResult):
    raise HTTPException(404, "Target user not found") 
