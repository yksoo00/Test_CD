import sys

sys.path.append("app/")

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


from models import *

# DB 스키마 생성
Base.metadata.create_all(bind=engine)


def clear_db():
    meta = MetaData()
    meta.reflect(bind=engine)
    with engine.connect() as conn:
        for table in reversed(meta.sorted_tables):
            conn.execute(table.delete())
        conn.commit()
