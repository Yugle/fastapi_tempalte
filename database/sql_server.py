from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from conf.config import config

sql_config = config.sql_server

engine = create_engine(
    # "mssql+pyodbc://sa:sa@10.8.140.233:1433/TestDB?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes&Encrypt=no",
    f"mssql+pymssql://{sql_config.username}:{sql_config.password}@{sql_config.host}:{sql_config.port}/{sql_config.db_name}",
    isolation_level="REPEATABLE READ"
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
