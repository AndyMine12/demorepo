from pydantic import BaseModel, Field, EmailStr

class DirectoryDTO(BaseModel):
  name: str
  emails: list[EmailStr]