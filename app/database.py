from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from sqlalchemy import MetaData
from sqlalchemy.pool import StaticPool

if os.getenv("TESTING") == "True":
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    engine = create_engine(os.getenv("DATABASE_URL"))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def clear_db():
    meta = MetaData()
    meta.reflect(bind=engine)
    with engine.connect() as conn:
        for table in reversed(meta.sorted_tables):
            conn.execute(table.delete())
        conn.commit()
