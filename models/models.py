from database.db import Base, async_engine

from models.contacts import Contact
from models.users import User

Base.metadata.create_all(bind=async_engine)
