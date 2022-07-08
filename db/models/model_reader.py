class ModelReader:
	def __init__(self, table_cls) -> None:
		self._table_cls = table_cls

	def get_columns(self):
		return self._table_cls.columns._all_columns

	def filter(self, *args):
		pass

	def create_record(self, **kwargs):
		pass
		