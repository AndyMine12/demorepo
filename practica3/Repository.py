
import practica3.directory
from practica3.directory import Directory, Email
from practica3.directoryDTO import DirectoryResponseDTO
from sqlmodel import Session, select

class DirectoryRepository():
  def __init__(self, engine):
    self.engine = engine
    
  
  def get_count(self) -> int:
    pass

  def find_all(self, page: int, perpage: int) -> list[Directory]:
    pass

  def find_by_id(self, id: int) -> Directory:
    with Session(self.engine) as session:
      query = select(Directory, Email.content).where(Directory.id == id).where(Email.directory_id == Directory.id)
      resultIter = session.exec(query)
      
      resultemails = []
      for item,email in resultIter:
        resultid = item.id
        resultname = item.name
        resultemails.append(email)
      result = DirectoryResponseDTO(id=resultid, name=resultname, emails=resultemails)
        
      return result

  def create(self, name: str, emails: list[str]) -> Directory:
    newEmails = [Email(content=email) for email in emails]
    newDirectory: Directory = Directory(name=name, emails=newEmails)
    with Session(self.engine) as session:
      session.add(newDirectory)
      session.commit()
      session.refresh(newDirectory)
      return newDirectory


  def update(self, id: int, name: (str | None) = None, emails: (list[str] | None) = None) -> Directory:
    with Session(self.engine) as session:
      result = session.exec(select(Directory).where(Directory.id == id))
      updatingDirectory:Directory = result.one()
      #prevDirectory:DirectoryResponseDTO = self.find_by_id(id)
      #updatingDirectory:Directory = Directory(id=prevDirectory.id, name=prevDirectory.name, emails=prevDirectory.emails)

      if name is not None:
        updatingDirectory.name = name

      if emails is not None:
        updatingDirectory.emails = [Email(content=email) for email in emails]
      else:
        updatingDirectory.emails = []
        query = session.exec(select(Email.content).where(Email.directory_id == id))
        for item in query:
          updatingDirectory.emails.append(Email(content=item))

      session.add(updatingDirectory)
      session.commit()
      session.refresh(updatingDirectory)
      return updatingDirectory

  def delete(self, id: int) -> bool:
    pass