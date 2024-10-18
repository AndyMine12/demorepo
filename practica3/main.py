from fastapi import FastAPI

app = FastAPI()


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
def create_directory(name: str, emails: list[str]):
  return "Not Implemented"

@app.put("/directories/{id}")
def update_directory(id: int):
  return "Not Implemented"

@app.patch("/directories/{id}")
def partially_update_directory(id: int):
  return "Not Implemented"

@app.delete("/directories/{id}")
def delete_directory_by_id(id: int):
  return "Not Implemented"
