
import practica3.directory
from practica3.directory import Directory, Email
from sqlmodel import Session

class DirectoryRepository():
  def __init__(self, engine):
    self.engine = engine
    
  
  def get_count(self) -> int:
    pass

  def find_all(self, page: int, perpage: int) -> list[Directory]:
    pass

  def find_by_id(self, id: int) -> Directory:
    pass

  def create(self, name: str, emails: list[str]) -> Directory:
    newEmails = [Email(content=email) for email in emails]
    newDirectory: Directory = Directory(name=name, emails=newEmails)
    with Session(self.engine) as session:
      session.add(newDirectory)
      session.commit()
      session.refresh(newDirectory)
      return newDirectory
    pass


  def update(self, id: int, name: (str | None) = None, emails: (list[str] | None) = None) -> Directory:
    pass

  def delete(self, id: int) -> bool:
    pass