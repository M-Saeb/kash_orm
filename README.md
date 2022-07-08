# Kash ORM
Build, edit and delete SQL tabels, And record on the run.
KashORM allows to intreact with a datbase without need to definning static models for it.
Used for systems that require editing databased on the run

*This is still underconstruction, so many of what's writting here is still not developed*

## Structor
![Diagram image](docs/db_library_diagram.png)
- KashORM build on top of SQLAlchemy, in a way that standarize the code for all databases so that the user woudn't need to worry about the selected database


## Tests
- Using [PyTest](https://docs.pytest.org/en/7.1.x/) as the testing framwork for this project 


## Usefull Links
some usefull docs pages that I'm using for the project:
- SQL Alchemy with autoload [link](https://www.blog.pythonlibrary.org/2010/09/10/sqlalchemy-connecting-to-pre-existing-databases/) and [link2](https://gtpedrosa.github.io/blog/using-sqlalchemy-to-navigate-an-existing-database/)
- SQL Alchemy with automp [link](https://docs.sqlalchemy.org/en/14/orm/extensions/automap.html)
- SQLAlchemy AuthMap [link](https://docs.sqlalchemy.org/en/14/orm/extensions/automap.html)
- SQLAlchemy Class mapping API [link](https://docs.sqlalchemy.org/en/14/orm/mapping_api.html#sqlalchemy.orm.registry.map_imperatively)

