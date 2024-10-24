
import src.directory
from src.directory import Directory, Email
from src.directoryDTO import DirectoryResponseDTO
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
      offset:int = round((page - 1)*perpage)
      queryResult = session.exec(select(Directory).offset(offset).limit(perpage))
      resultList = []
      for item in queryResult:
        resultList.append(self.find_by_id(item.id))
      return resultList

  def find_by_id(self, id: int) -> Directory:
    with Session(self.engine) as session:
      query = select(Directory, Email.content).where(Directory.id == id).where(Email.directory_id == Directory.id)
      resultIter = session.exec(query)
      
      resultid = None
      resultname = None
      resultemails = []
      for item,email in resultIter:
        resultid = item.id
        resultname = item.name
        resultemails.append(email)
      if resultid is None:
        return None
      result = DirectoryResponseDTO(id=resultid, name=resultname, emails=resultemails)
        
      return result

  def create(self, name: str, emails: list[str]) -> DirectoryResponseDTO:
    newEmails = [Email(content=email) for email in emails]
    newDirectory: Directory = Directory(name=name, emails=newEmails)
    with Session(self.engine) as session:
      session.add(newDirectory)
      session.commit()
      session.refresh(newDirectory)

      return DirectoryResponseDTO(id= newDirectory.id, name= newDirectory.name, emails= emails)


  def update(self, id: int, name: (str | None) = None, emails: (list[str] | None) = None) -> DirectoryResponseDTO:
    with Session(self.engine) as session:
      result = session.exec(select(Directory).where(Directory.id == id))
      updatingDirectory:Directory = result.first()
      if updatingDirectory is None:
        return None

      if name is not None:
        updatingDirectory.name = name

      updatingEmails: list[Email]
      if emails is not None:
        updatingEmails = [Email(content=email) for email in emails]
      else:
        prevDirectory:DirectoryResponseDTO = self.find_by_id(id)
        updatingEmails = [Email(content=email) for email in prevDirectory.emails]

      updatingDirectory.emails = updatingEmails

      session.add(updatingDirectory)
      session.commit()
      session.refresh(updatingDirectory)
    
      return DirectoryResponseDTO(id= updatingDirectory.id, name= updatingDirectory.name, emails= [str(email) for email in updatingEmails])

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