from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from models.engine import get_engine

Base = automap_base()

engine = get_engine()

# reflect the tables
Base.prepare(engine, reflect=True)

Src = Base.classes.src
War = Base.classes.war
Effective = Base.classes.eff_atks
Tags = Base.classes.tags
Public_v0 = Base.classes.public_v0

# For eff_ackts table, refer db_mysql.py

