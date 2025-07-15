from sqlmodel import Session, create_engine

DATABASE_URL = "sqlite:///./database.db"  # Cambiar si usás Postgres/MySQL

engine = create_engine(DATABASE_URL, echo=False)

def get_session():
    with Session(engine) as session:
        yield session

