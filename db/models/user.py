from pydantic import BaseModel
from typing import Optional

#Entidad usuario
class User(BaseModel):
  id: Optional[str] = None #Opcional
  username: str
  email: str