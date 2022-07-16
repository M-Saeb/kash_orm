from typing import List
from sqlalchemy import Table, Column
from sqlalchemy.sql.schema import MetaData
from .. import fields

class ModelCreator:
	"""
		This class handles creating the ORM object, 
		writing it on the database happens from the DB class
	"""
	def __init__(self, model_name) -> None:
		self.model_name =  model_name
		self.columns = []

	def set_metadata(self, metadata_object: MetaData):
		self.metadata = metadata_object

	def add_column(self, col_name: str, col_cls: fields.BaseField):
		kwargs = col_cls._kwargs
		new_column = Column(col_name, col_cls, **kwargs)
		self.columns.append(new_column)

	def set_columns(self, columns: List[Column]):
		self.columns = columns

	def generate_table_class(self):
		primary_key_is_defined = any( map(lambda col: getattr(col, "primary_key", False), self.columns) ) 
		assert primary_key_is_defined, "No primary key column was provided"
		table_cls = Table(
			self.model_name,
			self.metadata,
			*self.columns,
		)
		return table_cls

class ModelUpdater:
	"""
		This class hold all the model updater functions/operations,
		each function returns a query to run from the DB class
	"""

	def __init__(self, model_name):
		self.model_name =  model_name

	def create_columns(self, *args, **columns) -> List[str]:
		assert len(args) == 0, "create_columns() doesn't take list arguments"
		assert len(columns) > 0, "no key arguments were provided"
		query_str = f'ALTER TABLE {self.model_name} '
		for col_name, col_cls in columns.items():
			assert isinstance(col_cls, fields.BaseField), f"The value for {col_name} must be a KASH ORM field"
			col_type = col_cls.psql_col_name
			query_str += f'ADD COLUMN {col_name} {col_type}, '
		query_str = query_str[:-2] + ";"
		return query_str

	def update_columns(self, *args, **kwargs):
		assert len(args) == 0, "update_columns() doesn't take list arguments"
		assert len(kwargs) > 0, "no key arguments were provided"
		query_str = f'ALTER TABLE {self.model_name} '
		for col_name, col_cls in kwargs.items():
			assert isinstance(col_cls, fields.BaseField), f"The value for {col_name} must be a KASH ORM field"
			col_type = col_cls.psql_col_name
			query_str += f"ALTER COLUMN {col_name} TYPE {col_type}, "

		query_str = query_str[:-2] + ";"
		return query_str

	def delete_columns(self, *columns, **kwargs):
		assert len(columns) > 0, "to arguments/column names were provided"
		assert len(kwargs) == 0, "delete_columns() doesn't take key arguments"
		query_str = f'ALTER TABLE {self.model_name} '
		for col_name in columns:
			query_str += f'DROP COLUMN {col_name}, '
		query_str = query_str[:-2] + ";"
		return query_str
