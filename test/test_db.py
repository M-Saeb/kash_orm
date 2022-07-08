from db import DB
import pytest

class TestDB:
	def test_db_connection(self, tmp_path):
		tmp_path.mkdir()
		demo_db_path = tmp_path / "demo.db"
		test_db = DB(demo_db_path)

	def test_creating_model(self):
		pass

	def test_reading_model(self):
		pass

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
