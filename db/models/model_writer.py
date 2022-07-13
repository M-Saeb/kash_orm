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
		assert primary_key_is_defined, "No primary key column was provided"
		new_table = Table(
			self.model_name,
			self.metadata,
			*self.columns,
		)
		return new_table

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
		for col_name, col_dict in columns.items():
			col_type = col_dict["type"].upper()
			query_str += f'ADD COLUMN {col_name} {col_type}, '
		query_str = query_str[:-2] + ";"
		return query_str

	def update_columns(self, *args, **kwargs):
		assert len(args) == 0, "update_columns() doesn't take list arguments"
		assert len(kwargs) > 0, "no key arguments were provided"
		query_str = f'ALTER TABLE {self.model_name} '
		for col_name, to_update_dict in kwargs.items():
			assert isinstance(to_update_dict, dict), "the value for update_columns() kwargs must be dictionaries"
			assert to_update_dict.get("update"), f"This update dict ({to_update_dict}) is not handled yet"
			new_data_type = to_update_dict["type"].upper()
			query_str += f"ALTER COLUMN {col_name} TYPE {new_data_type}, "

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
