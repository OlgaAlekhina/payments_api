from fastapi import APIRouter, HTTPException, status
from app.users.auth import get_password_hash
from app.users.dao import UsersDAO

from .auth import authenticate_user
from .schemas import UserAuth


users_router = APIRouter(prefix='/users', tags=['Auth'])


@users_router.post("/login/", summary="Авторизация пользователей")
async def auth_user(response: Response, user_data: UserAuth):
    check = await authenticate_user(email=user_data.email, password=user_data.password)
    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Пользователь с такими учетными данными не найден')
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {'access_token': access_token, 'refresh_token': None}