from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('postgresql://myuser:mypass@localhost/mybase', echo=True)

Base = declarative_base()

Session = sessionmaker()