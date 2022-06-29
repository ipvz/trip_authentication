from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter, status, Depends
from database import Session, engine
from schemas import SingUpModel, LoginModel
from models import User
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash

auth_router = APIRouter(
    prefix='/auth'
)

session = Session(bind=engine)


@auth_router.get('/')
async def hello(Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return {'hello': 'from auth'}


@auth_router.post('/singup', status_code=status.HTTP_201_CREATED)
async def singup(user: SingUpModel):
    db_email = session.query(User).filter(User.email==user.email).first()
    if db_email is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with the email already exitst")
    db_username = session.query(User).filter(User.username==user.username).first()
    if db_username is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with the username already exitst")

    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=True,
        is_staff=user.is_staff
    )
    session.add(new_user)
    session.commit()
    return new_user


@auth_router.post('/login')
async def login(user: LoginModel, Authorize: AuthJWT=Depends()):
    db_user = session.query(User).filter(User.username==user.username).first()
    if db_user and check_password_hash(db_user.password, user.password):
        access_token = Authorize.create_access_token(subject=db_user.username)
        refresh_token = Authorize.create_refresh_token(subject=db_user.username)
        response = {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
        return jsonable_encoder(response)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Username or Password")


@auth_router.get('/refrsh')
async def refresh_token(Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_refresh_token_required()
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Please provide a valid refresh token')
    current_user = Authorize.get_jwt_subject()
    access_token = Authorize.create_access_token(subject=current_user)
    return jsonable_encoder({"access_token": access_token})
