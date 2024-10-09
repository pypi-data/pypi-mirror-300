import json
import sqlite3
from logging import Logger
from typing import Dict, List, Optional, TypeVar, Type
from anlogger import Logger as AnLogger
from pydantic import BaseModel, create_model
from ansqlite.exceptions import (
    DatabaseInitializationException,
    ModelNotFoundException,
    TransactionException
)
from ansqlite.schema import TableColumn, PrimaryKeyType
from ansqlite.utils import trace

T = TypeVar('T', bound=BaseModel)


class Database:
  def __init__(
      self,
      database_path: str,
      schemas: Dict[str, List[TableColumn]],
      logger: Optional[Logger] = None
  ):
    super().__init__()
    self.logger = logger if logger is not None else AnLogger(
        name='ansqlite', default_loglevel='INFO').get()

    self.schemas: Dict[str, List[TableColumn]] = schemas
    self.models: Dict[str, Type[BaseModel]] = {}

    try:
      self.dbconn = sqlite3.connect(database_path)
    except Exception as e:
      self.logger.critical(trace('Failed to open database', e))
      raise DatabaseInitializationException('Failed to open database') from e

    for table_name, schema in self.schemas.items():
      self.init_table(table_name=table_name, table_schema=schema)

  def init_table(self, table_name: str, table_schema: List[TableColumn]) -> None:
    column_sql = []
    model_entries = {}
    schema = [TableColumn.model_validate(col) for col in table_schema]

    def pk_desc(x: TableColumn) -> str:
      return ' DESC' if x.primary_key is PrimaryKeyType.Descending else ''
    pk_cols = [
        f'{x.name}{pk_desc(x)}' for x in schema if x.primary_key is not None]
    pk_text = f'PRIMARY KEY ({", ".join(pk_cols)})' if len(
        pk_cols) > 0 else None

    for col in schema:
      not_nullable = col.nullable is False
      is_required = False if col.primary_key is PrimaryKeyType.Autoincrementing else not_nullable
      s = [
          col.name,
          col.datatype.name
      ]
      if col.primary_key is None:
        if not_nullable is True:
          s.append('NOT NULL')
        if col.unique is True:
          s.append('UNIQUE')
      column_sql.append(' '.join(s))

      model_entries[col.name] = (
          col.datatype.value, ... if is_required else None) if not_nullable else (
          col.datatype.value | None, ... if is_required else None)

    if pk_text is not None:
      column_sql.append(pk_text)

    self.models[table_name] = create_model(table_name, **model_entries)

    try:
      cur = self.dbconn.cursor()
      cur.execute(
          f'CREATE TABLE IF NOT EXISTS {table_name} ({", ".join(column_sql)});')
      self.schemas[table_name] = table_schema

    except Exception as e:
      self.logger.error(trace('Failed to initialize table', e))
      raise DatabaseInitializationException(
          'Failed to initialize table') from e

  def get_model(self, table_name: str) -> Type[BaseModel]:
    if table_name not in self.models:
      raise ModelNotFoundException(f'Model not found for table "{table_name}"')
    return self.models[table_name]

  def get_connection(self) -> sqlite3.Connection:
    return self.dbconn

  def insert_data(
      self,
      table_name: str,
      data: List[BaseModel],
  ) -> None:
    if len(data) < 1:
      return

    self.logger.debug(
        'Insert data to table %s: %s',
        table_name,
        json.dumps([row.model_dump() for row in data], indent=2)
    )

    model = self.models[table_name] if table_name in self.models else None
    if model is None:
      raise DatabaseInitializationException(
          f'Table "{table_name}" has not been initialized; inserting data failed')

    cols = model.model_validate(data[0].model_dump()).model_dump().keys()
    rowdata = [tuple(model.model_validate(row.model_dump()).model_dump().values())
               for row in data]

    try:
      cur = self.dbconn.cursor()
      cur.executemany(
          ' '.join([
              f'INSERT OR IGNORE INTO {table_name}',
              f'({", ".join(cols)}) VALUES ({", ".join("?"*len(cols))})'
          ]),
          rowdata
      )
      self.dbconn.commit()
    except Exception as e:
      self.logger.error(trace('Failed to insert data', e))
      raise TransactionException('Failed to insert data') from e

  def execute_and_fetchall(
          self, sql: str, errmsg: str, result_model: Type[T]) -> List[T]:
    try:
      cur = self.dbconn.cursor()
      res = cur.execute(sql)
      rows = res.fetchall()
      cols = [description[0] for description in cur.description]
      data = [result_model(**dict(zip(cols, row))) for row in rows]
      return data
    except Exception as e:
      self.logger.error(trace(errmsg, e))
      raise TransactionException(errmsg) from e

  def execute_and_commit(self, sql: str, errmsg: str) -> None:
    try:
      cur = self.dbconn.cursor()
      cur.execute(sql)
      self.dbconn.commit()
    except Exception as e:
      self.logger.error(trace(errmsg, e))
      raise TransactionException(errmsg) from e
