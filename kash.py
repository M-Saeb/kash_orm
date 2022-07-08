from sqlalchemy import Integer, String
from db import DB
""" This file is sandboox at the moment"""


new_db = DB("demo.db")

model_class = new_db.get_model("event")
print(model_class)