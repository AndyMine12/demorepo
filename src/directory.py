from sqlmodel import Field, SQLModel, Column, Relationship

class Directory(SQLModel, table=True):
  id: int | None = Field(default=None,  primary_key=True)
  name: str
  emails: list["Email"] = Relationship(back_populates="directory")

class Email(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  content: str
  directory_id: int | None = Field(default=None, foreign_key="directory.id")
  directory: Directory | None = Relationship(back_populates="emails")

  def __str__(self):
    return f"{self.content}"
  
  def __repr__(self):
    return self.__str__()