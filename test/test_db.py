from db import DB
from sqlalchemy import Column, Integer, String
import testing.postgresql
import pytest

class TestDB:

	def _creat_db_engine(self, db_path) -> DB:
		with testing.postgresql.Postgresql() as postgresql:
			test_db = DB(postgresql)
			return test_db

	def _create_model(self, db: DB):
		model = db.create_model("test_table",
			id={"type": "Integer", "kwargs": {"primary_key": True}},
			name={"type": "String"},
			age={"type": "String"},
		)
		return model

	def test_db_connection(self, tmp_path):
		test_db = self._creat_db_engine(tmp_path)

	def test_creating_model(self, tmp_path):
		test_db = self._creat_db_engine(tmp_path)
		test_model = self._create_model(test_db)
		print(test_model)
		assert test_model, "Something went wrong when creating a model"

	def test_reading_model(self, tmp_path):
		test_db = self._creat_db_engine(tmp_path)
		test_model = self._create_model(test_db)
		test_model = test_db.get_model("test_table")
		print(test_model)
		model_columns = test_model.get_columns()
		print("model_columns", model_columns)
		assert len(model_columns) == 3
		id_column = model_columns[0]
		name_column = model_columns[1]
		type_column = model_columns[2]
		assert id_column.name == "id"
		assert name_column.name == "name"
		assert type_column.name == "age"

	def test_updating_model_createing_new_columns(self, tmp_path):
		model_name = "test_table"
		test_db = self._creat_db_engine(tmp_path)
		test_model = self._create_model(test_db)
		test_db.update_model(
			model_name=model_name,
			op="create_columns",
			id_number={"type": "String"},
			points={"type": "String"}
		)
		model_class = test_db.get_model(model_name)
		columns = model_class.get_columns()
		id_column = columns[3]
		points_column = columns[4]
		assert id_column.name == "id_number"
		assert points_column.name == "points"

	def test_updating_model_deleting_columns(self, tmp_path):
		model_name = "test_table"
		# test_db = self._creat_db_engine(tmp_path)
		# test_model = self._create_model(test_db)
		# test_db.update_model(model_name, "delete_columns", "name", "age")
		# model_class = test_db.get_model(model_name)
		# columns = model_class.get_columns()
		# assert len(columns) == 1
		# assert columns[0].name == "id"

	def test_updating_model_updating_existing_columns(self, tmp_path):
		pass

	def test_deleting_model(self):
		pass

	def test_creating_record(self):
		pass

	def test_updating_record(self):
		pass

	def test_deleting_record(self):
		pass
