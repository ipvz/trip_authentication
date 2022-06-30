from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config.settings import Config, Settings

cfg = Config.parse_file('config/Config.yaml')

settings = Settings(**cfg.psql)

engine = create_engine(settings.DATABASE_URI, echo=True)

Base = declarative_base()

Session = sessionmaker()