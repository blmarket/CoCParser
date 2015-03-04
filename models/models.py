from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from engine import get_engine

Base = automap_base()

engine = get_engine()

# reflect the tables
Base.prepare(engine, reflect=True)

print Base.classes

Src = Base.classes.src
War = Base.classes.war
Effective = Base.classes.eff_atks
Tags = Base.classes.tags

session = Session(engine)

q = session.query(War)

print q.count()

# # mapped classes are now created with names by default
# # matching that of the table name.
# User = Base.classes.user
# Address = Base.classes.address
# 
# session = Session(engine)
# 
# # rudimentary relationships are produced
# session.add(Address(email_address="foo@bar.com", user=User(name="foo")))
# session.commit()
# 
# # collection-based relationships are by default named
# # "<classname>_collection"
# print (u1.address_collection)


