# Kash ORM
Build, edit and delete SQL tabels, And record on the run.
KashORM allows to intreact with a datbase without need to definning static models for it.
Used for systems that require easy edit on the Database

*This project is still just a concept, some diagrams and detailed explanation can be found in the `docs` directory*

## Method to implement this
You could probably tell, it is not done yet
I'm still looking over the recourses to build this. some possible choices are:
- SQL Alchemy with autoload (link)[https://www.blog.pythonlibrary.org/2010/09/10/sqlalchemy-connecting-to-pre-existing-databases/] and (link2)[https://gtpedrosa.github.io/blog/using-sqlalchemy-to-navigate-an-existing-database/]
- SQL Alchemy with automp (link)[https://docs.sqlalchemy.org/en/14/orm/extensions/automap.html] (this seems like the best approach)
- BIGSQL which is a python project I found on Github(link)[https://github.com/wabscale/bigsql]


## Usefull Links
some usefull links are:
- SQLAlchemy AuthMap (link)[https://docs.sqlalchemy.org/en/14/orm/extensions/automap.html]
- SQLAlchemy Class mapping API (link)[https://docs.sqlalchemy.org/en/14/orm/mapping_api.html#sqlalchemy.orm.registry.map_imperatively]

