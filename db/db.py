from typing import List, Dict
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, registry
from sqlalchemy import create_engine, Column
from .models import ModelCreator, ModelReader, ModelUpdater

class DB:
	def __init__(self, host, dbname, port=5432) -> None:
		self._base = automap_base()
		db_url = f'postgresql+psycopg2://postgres:@{host}:{port}/{dbname}'
		self._egnine = create_engine(db_url)
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
		model_creator_obj = ModelCreator(model_name)
		model_creator_obj.set_metadata(self._mapper_registry.metadata)
		for col_name, col_dict in columns.items():
			assert isinstance(col_dict, dict), f"the value for {col_name} must be dict"
			assert col_dict.get("type"), f"No 'type' key was provided in the dict for {col_name}"
			type_name = col_dict["type"]
			kwargs = col_dict.get("kwargs", {})
			type_class = getattr(sqlalchemy, type_name, None)
			if not type_class:
				raise KeyError(f"The given column name {type_name} does not exist")
		
			model_creator_obj.add_column(
				column_name=col_name,
				column_type=type_class,
				**kwargs
			)
		table_cls = model_creator_obj.generate_table_class()
		model_cls = type(model_name, (self._base, ) , {"__tablename__": model_name} )
		self._mapper_registry.map_imperatively(model_cls, table_cls)
		self._mapper_registry.metadata.create_all() # this line is where the SQL table creation happens
		table_class = self.get_model(model_name)
		return table_class

	def update_model(self,
		model_name,
		op,
		*args,
		**kwargs
	) -> None:
		"""
			update database model according to the given params
			:param `model_name`: model to update
			:param `op`: the name of the opertaion to preform
			:param `args` and `kwargs`: each operation has a different proccess, some take List argument, other take Dict arguments,
			The `args` and `kwargs` are passed directly to the operation function to cover all the function needs.
			Expcetions are handled through each operation function
		"""
		assert len(kwargs) or len(args), "No args or kwargs were provided for the operation"
		model_updater_cls = ModelUpdater(model_name)
		op_func = getattr(model_updater_cls, op, None)
		if not op_func:
			raise ValueError(f"There request update operation {op} was not found in ModeUpdater")
		op_queries = op_func(*args, **kwargs)
		assert op_queries, f"the updater function {op_func} didn't resturn any query"
		self._connection.execute(op_queries)
		
	def get_model(self, model_name):
		self._reset_base()
		orm_classes = self._base.classes
		model_obj = getattr(orm_classes, model_name, None)
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

	def delete_model(self, model_name):
		pass