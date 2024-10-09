from enum import Enum
from typing import Optional
from pydantic import BaseModel


class Datatype(Enum):
  INTEGER = int
  REAL = float
  TEXT = str
  BLOB = bytes


class PrimaryKeyType(Enum):
  Ascending = 'ASC'
  Descending = 'DESC'
  Autoincrementing = 'AUTOINCREMENT'


class TableColumn(BaseModel):
  name: str
  datatype: Datatype
  nullable: Optional[bool] = False
  primary_key: Optional[PrimaryKeyType] = None
  unique: Optional[bool] = False
