from typing import List, Dict
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, registry
from sqlalchemy import create_engine
from . import ModelCreator

class DB:
	def __init__(self, db_path) -> None:
		self._base = automap_base()
		self._egnine = create_engine("sqlite:///%s" % (db_path))
		self._base.prepare(autoload_with=self._egnine)
		self._session = Session(self._egnine)
		self._mapper_registry = registry(_bind=self._egnine)

	def create_model(self, model_name, columns: List[Dict[str, any]]):
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
		for col in columns:
			kwargs = col.get("kwargs", {})
			model_obj.add_column(
				column_name=col["name"],
				column_type=col["type"],
				**kwargs
			)
		table_obj = model_obj.return_table_object()
		model_class = type(model_name, (self._base,) , {"__tablename__": model_name} )
		self._mapper_registry.map_imperatively(model_class, table_obj)
		self._mapper_registry.metadata.create_all()
		return model_class

	def update_model(self, model_name, columns):
		pass

	def delete_model(self, model_name):
		pass

	def get_model(self, model_name):
		base_classes = self._base.classes
		model_class = getattr(base_classes, model_name)
		return model_class

	def search_models(self, *args):
		pass