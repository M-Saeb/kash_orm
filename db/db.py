from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

class DB:
	def __init__(self, db_path) -> None:
		self._base = automap_base()
		self._egnine = create_engine("sqlite:///%s" % (db_path))
		self._base.prepare(autoload_with=self._egnine)
		self._session = Session(self._egnine)

	def create_model(self, model_name, columns):
		pass

	def update_model(self, model_name, columns):
		pass

	def delete_model(self, model_name):
		pass

	def get_model(self, model_name):
		pass

	def search_models(self, *args):
		pass