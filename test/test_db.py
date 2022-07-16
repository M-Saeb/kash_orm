from db import DB, fields
import pytest

class TestDB:

	@pytest.fixture
	def db_cls(self, postgresql) -> DB:
		db_cls = DB(host=postgresql.info.host, dbname=postgresql.info.dbname, port=postgresql.info.port)
		return db_cls

	@pytest.fixture
	def model_name(self) -> str:
		return "test_model"

	@pytest.fixture
	def db_cls_with_test_model(self, db_cls: DB, model_name: str) -> DB:
		db_cls.create_model(model_name,
			id=fields.Integer(primary_key=True),
			name=fields.String(),
			age=fields.String(),
		)
		return db_cls


	def test_db_connection(self, db_cls: DB):
		test_db = db_cls

	def test_creating_model(self, db_cls_with_test_model: DB):
		print(db_cls_with_test_model)
		assert db_cls_with_test_model, "Something went wrong when creating a model"

	def test_reading_model(
		self,
		db_cls_with_test_model: DB,
		model_name
	):
		test_model = db_cls_with_test_model.get_model(model_name)
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

	def test_updating_model_createing_new_columns(
		self,
		db_cls_with_test_model: DB,
		model_name
	):
		db_cls_with_test_model.update_model(
			model_name=model_name,
			op="create_columns",
			id_number=fields.String(),
			points=fields.String()
		)
		model_class = db_cls_with_test_model.get_model(model_name)
		columns = model_class.get_columns()
		id_column = columns[3]
		points_column = columns[4]
		assert len(columns) == 5
		assert id_column.name == "id_number"
		assert points_column.name == "points"

	def test_updating_model_deleting_columns(
		self,
		db_cls_with_test_model: DB,
		model_name
	):
		db_cls_with_test_model.update_model(model_name, "delete_columns", "name", "age")
		model_class = db_cls_with_test_model.get_model(model_name)
		columns = model_class.get_columns()
		assert len(columns) == 1
		assert columns[0].name == "id"

	def test_updating_model_updating_existing_columns_changing_column_type(
		self,
		db_cls_with_test_model: DB,
		model_name
	):
		db_cls = db_cls_with_test_model
		db_cls.update_model(
			model_name,
			"update_columns",
			name=fields.String()
		)
		model_obj = db_cls.get_model(model_name)
		columns = model_obj.get_columns()
		name_column = columns[1]
		# assert isinstance(name_column.type, VARCHAR)
		print(name_column)

	def test_updating_model_updating_existing_columns_renaming(self, db_cls: DB):
		pass

	def test_deleting_model(self):
		pass

	def test_creating_record(self):
		pass

	def test_updating_record(self):
		pass

	def test_deleting_record(self):
		pass
