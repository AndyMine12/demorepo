
import practica3.directory
from practica3.directory import Directory, Email
from practica3.directoryDTO import DirectoryResponseDTO
from sqlmodel import Session, select

class DirectoryRepository():
  def __init__(self, engine):
    self.engine = engine
    
  
  def get_count(self) -> int:
    with Session(self.engine) as session:
      result = session.exec(select(Directory))
      count = 0
      for item in result:
        count += 1
      return count

  def find_all(self, page: int, perpage: int) -> list[Directory]:
    with Session(self.engine) as session:
      queryResult = session.exec(select(Directory).offset((page-1)*perpage).limit(perpage).where(Directory.id == id))
      resultList = []
      for item in queryResult:
        resultList.append(self.find_by_id(item.id))
      return resultList

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
      updatingDirectory:Directory = result.first()

      prevDirectory:DirectoryResponseDTO = self.find_by_id(id)
      prevEmails = [Email(content=email) for email in prevDirectory.emails]
      updatingDirectory.emails = prevEmails

      if name is not None:
        updatingDirectory.name = name

      if emails is not None:
        updatingDirectory.emails = [Email(content=email) for email in emails]

      session.add(updatingDirectory)
      session.commit()
      session.refresh(updatingDirectory)
      return updatingDirectory

  def delete(self, id: int) -> bool:
    with Session(self.engine) as session:
      statement = select(Directory).where(Directory.id == id)
      results = session.exec(statement)
      direc = results.first()
      if direc is None:
        return False
      session.delete(direc)
      session.commit()
      return True