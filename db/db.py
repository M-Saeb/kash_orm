from typing import List, Dict
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, registry
from sqlalchemy import create_engine, Column
from .models import ModelCreator, ModelReader, ModelUpdater

class DB:
	def __init__(self, db_path) -> None:
		self._base = automap_base()
		self._egnine = create_engine("sqlite:///%s" % (db_path))
		self._connection = self._egnine.connect()
		self._base.prepare(autoload_with=self._egnine)
		self._session = Session(self._egnine)
		self._mapper_registry = registry(_bind=self._egnine)

	def create_model(self, model_name, **columns):
		"""
			Create models in the database 
			:param `model_name`: the name of both the model & SQL table
			:param `columns`: a list of dictionary for the tables columns in the following format:
				[
					{
						"name": str, // column name
						"type": TypeEgine, // column type (uses SQLAlchemy columns types)
						"kwargs": {} // key argument that you want to pass to to the column
					}, ...
				]
		"""
		model_obj = ModelCreator(model_name)
		model_obj.add_metadata(self._mapper_registry.metadata)
		for col_name, col_dict in columns.items():
			type_name = col_dict["type"]
			kwargs = col_dict.get("kwargs", {})
			type_class = getattr(sqlalchemy, type_name, None)
			if not type_class:
				raise KeyError(f"The given column name {type_name} does not exist")
		
			model_obj.add_column(
				column_name=col_name,
				column_type=type_class,
				**kwargs
			)
		table_obj = model_obj.return_table_object()
		model_class = type(model_name, (self._base, object) , {"__tablename__": model_name} )
		self._mapper_registry.map_imperatively(model_class, table_obj)
		self._mapper_registry.metadata.create_all()
		table_class = self.get_model(model_name)
		return table_class

	def update_model(self,
		model_name,
		op="create_columns",
		**columns
	) -> None:
		"""
			update database model according to the given params
			:param `model_name`: model to update
			:param `op`: opertaion to preform
			:param `columns`: takes a list of columns to create in the table
		"""
		assert len(columns) > 0, "No columns were provided for the operation"
		model_updater = ModelUpdater(model_name)
		op_func = getattr(model_updater, op, None)
		if not op_func:
			raise ValueError(f"There request update operation {op} was not found in ModeUpdater")
		op_queries = op_func(**columns)
		for query in op_queries:
			self._connection.execute(query)
		
	def delete_model(self, model_name):
		pass

	def get_model(self, model_name):
		self._reset_base()
		base_classes = self._base.classes
		model_obj = getattr(base_classes, model_name, None)
		if not model_obj:
			raise ValueError(f"model {model_name} was not found")
		table_object = model_obj.metadata.tables[model_name]
		model_class = ModelReader(table_object)
		return model_class

	def _reset_base(self):
		"""
			Reseting the _base class needs to happen manually.
			Which is what this _reset_base() is for
		"""
		self._base = automap_base()
		self._base.prepare(autoload_with=self._egnine)

	def search_models(self, *args):
		pass