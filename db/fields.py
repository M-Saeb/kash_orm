import enum
from typing import List
from abc import abstractmethod
from sqlalchemy import Text, Integer as SAInteg, Enum

# -----------------------------------------------
# from sqlalchemy import Integer, Enum

class MyEnum(enum.Enum):
    one = 1
    two = 2
    three = 3

# class MyClass(Base):
#     value = Column(Enum(MyEnum))
# -----------------------------------------------

class BaseField(): # Didn't add the ABC class cause it would conflict with SA meta class
	def __init__(self, *args, **kwargs) -> None:
		self._args = args
		self._kwargs = kwargs
		super().__init__()
	
	@property
	@abstractmethod
	def psql_col_name(self):
		return self.__visit_name__

class String(BaseField, Text):
	pass

class Integer(BaseField, SAInteg):
	pass


# TODO: This one isn't functional yet
class Selection(BaseField, Enum):
	# def __new__(cls, *args, **kwargs):
	# 	selection_tuple = args[0]
	# 	enum_cls_name = "SelectionEnum"
	# 	exec_string = f"class {enum_cls_name}(enum.Enum):\n"
	# 	for sel in selection_tuple:
	# 		exec_string += f"\t{sel[0]} = '{sel[1]}'\n"

	# 	enum_dict = {}
	# 	exec(exec_string, globals(), enum_dict)
	# 	enum_cls = enum_dict[ enum_cls_name ]
	# 	sl_enum_cls = Enum(enum_cls)
	# 	return sl_enum_cls

	def __init__(self, *args, **kwargs) -> None:
		selection_tuple = args[0]
		enum_cls_name = "SelectionEnum"
		exec_string = f"class {enum_cls_name}(enum.Enum):\n"
		for sel in selection_tuple:
			exec_string += f"\t{sel[0]} = '{sel[1]}'\n"

		enum_dict = {}
		exec(exec_string, globals(), enum_dict)
		enum_cls = enum_dict[ enum_cls_name ]
		kwargs["name"] = "column_name"
		super().__init__(enum_cls, *args[1:], **kwargs)