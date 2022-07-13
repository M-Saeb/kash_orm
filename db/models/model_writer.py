from typing import List
from sqlalchemy import Table, Column
from sqlalchemy.types import TypeEngine
from sqlalchemy.sql.schema import MetaData

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

	def add_column(self, column_name: str, column_type: TypeEngine, **kwargs):
		new_column = Column(column_name, column_type, **kwargs)
		self.columns.append(new_column)

	def set_columns(self, columns: List[Column]):
		self.columns = columns

	def generate_table_class(self):
		primary_key_is_defined = any( map(lambda col: getattr(col, "primary_key", False), self.columns) ) 
		if not primary_key_is_defined:
			raise ValueError("No primary key column was provided")
		new_table = Table(
			self.model_name,
			self.metadata,
			*self.columns,
		)
		return new_table

class ModelUpdater:
	""" This class creates SQL queries corresponding the requested operation """

	def __init__(self, model_name):
		self.model_name =  model_name

	def create_columns(self, *args, **columns) -> List[str]:
		assert len(args) == 0, "create_columns() doesn't take argument"
		queries = []
		for col_name, col_dict in columns.items():
			col_type = col_dict["type"].upper()
			query_line = f'ALTER TABLE {self.model_name} ADD {col_name} {col_type};'
			queries.append(query_line)
		return queries

	def update_columns(self, *columns, **kwargs):
		queries = []
		for col_name in columns:
			query_line = f'ALTER TABLE {self.model_name} DROP COLUMN {col_name};'
			queries.append(query_line)
		return queries

	def delete_columns(self, *columns, **kwargs):
		assert len(kwargs) == 0, "delete_columns() doesn't take key arguments"
		# cols_string = ", ".join(columns)
		# full_query = f'ALTER TABLE {self.model_name} DROP COLUMN {cols_string};'
		queries = []
		for col_name in columns:
			query_line = f'ALTER TABLE {self.model_name} DROP COLUMN {col_name};'
			queries.append(query_line)
		return queries
		# return full_query