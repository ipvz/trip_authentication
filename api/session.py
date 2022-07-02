from db.database import Session, engine
from crud.users import UserOperation

session = Session(bind=engine)
user_crud = UserOperation(session)
