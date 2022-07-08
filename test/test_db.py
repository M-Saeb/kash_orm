from db import DB
from sqlalchemy import Column, Integer, String
import pytest

class TestDB:
	def test_db_connection(self, tmp_path):
		demo_db_path = tmp_path / "demo.db"
		test_db = DB(demo_db_path)

	def test_creating_model(self, tmp_path):
		demo_db_path = tmp_path / "demo.db"
		test_db = DB(demo_db_path)
		test_model = test_db.create_model("test_table",
			id={"type": "Integer", "kwargs": {"primary_key": True}},
			name={"type": "String"},
			age={"type": "String"},
			
			)
		model_columns = test_model.get_columns()
		print(test_model)
		assert test_model, "Something went wrong when creating a model"
		print("model_columns", model_columns)
		assert len(model_columns) == 1
		id_column = model_columns[0]
		assert id_column._name == "id"

	def test_reading_model(self, tmp_path):
		demo_db_path = tmp_path / "demo.db"
		test_db = DB(demo_db_path)
		test_db.create_model("test_table",
			id={"type": "Integer", "kwargs": {"primary_key": True}},
			name={"type": "String"},
			age={"type": "String"},
			
			)
		model_test = test_db.get_model("test_table")
		print(model_test)

	def test_updateing_model(self):
		pass

	def test_deleting_model(self):
		pass

	def test_creating_record(self):
		pass

	def test_updating_record(self):
		pass

	def test_deleting_record(self):
		pass
