# conftest.py
import pytest
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from src.utils.database import Base, get_db
from src.main import app
from src.models.user import User as UserModel
from src.models.blog import Blog as BlogModel
from src.utils.hashing import bcrypt

DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSession = sessionmaker(bind=engine, autocommit=False, autoflush=False)


@pytest.fixture()
def db_session():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    db = TestingSession()

    # Create some mock users
    user1 = UserModel(id=1, username="u1", email="email1", password=bcrypt("password1"), is_admin=False)
    user2 = UserModel(id=2, username="u2", email="email2", password=bcrypt("password2"), is_admin=True)
    blog1 = BlogModel(title="b1", description="d1", user_id=1)
    db.add(user1)
    db.add(user2)
    db.add(blog1)
    db.commit()

    # Yield the db session to the test function
    yield db

    # After the test function is done, close the session and drop the tables
    db.close()
    Base.metadata.drop_all(bind=engine)


# Override the default dependency to use the test session
def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db