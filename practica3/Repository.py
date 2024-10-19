from sqlmodel import Session
from directory import Directory

class DirectoryRepository():
  def __init__(self):
    pass
  
  def get_count(self) -> int:
    pass

  def find_all(self, page: int, perpage: int) -> list[Directory]:
    pass

  def find_by_id(self, id: int) -> Directory:
    pass

  def create(self, name: str, emails: list[str]) -> Directory:
    pass

  def update(self, id: int, name: (str | None) = None, emails: (list[str] | None) = None) -> Directory:
    pass

  def delete(self, id: int) -> bool:
    pass