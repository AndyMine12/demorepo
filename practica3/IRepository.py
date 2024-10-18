class DirectoryRepository():
  def __init__(self, path: str):
    pass
  
  def get_count(self):
    pass

  def find_all(self):
    pass

  def find_by_id(self, id: int):
    pass

  def create(self, name: str, emails: list[str]):
    pass

  def update(self, id: int, name: (str | None) = None, emails: (list[str] | None) = None):
    pass

  def delete(self, id: int):
    pass