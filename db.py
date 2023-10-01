from sqlmodel import create_engine, Session

engine = create_engine(
    "postgresql://postgres:uccmagapp@localhost:5455/postgres",
    echo=True
)


def get_session():
    with Session(engine) as session:
        yield session
