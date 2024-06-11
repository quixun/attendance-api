from configs.database import Base
from pydantic import BaseModel
from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, text


class StudentSchema(BaseModel):
    id: str
    email: str
    name: str