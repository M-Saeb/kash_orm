from typing import List
from sqlalchemy import Table, Column
from sqlalchemy.types import TypeEngine
from sqlalchemy.sql.schema import MetaData

class ModelCreator:
	def __init__(self, model_name) -> None:
		self.model_name =  model_name
		self.columns = []

	def add_metadata(self, metadata_object: MetaData):
		self.metadata = metadata_object

	def add_column(self, column_name: str, column_type: TypeEngine, **kwargs):
		new_column = Column(column_name, column_type, **kwargs)
		self.columns.append(new_column)

	def set_columns(self, columns: List[Column]):
		self.columns = columns

	def return_table_object(self):
		primary_key_is_defined = any( map(lambda col: getattr(col, "primary_key", False), self.columns) ) 
		if not primary_key_is_defined:
			raise ValueError("No primary key column was provided")
		new_table = Table(
			self.model_name,
			self.metadata,
			*self.columns
		)
		return new_table
