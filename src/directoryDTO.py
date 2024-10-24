from pydantic import BaseModel, Field, EmailStr

class DirectoryDTO(BaseModel):
  name: str
  emails: list[EmailStr]

class DirectoryResponseDTO(BaseModel):
  id: int
  name: str
  emails: list[EmailStr]