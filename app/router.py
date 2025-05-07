from fastapi import APIRouter, HTTPException, status, Response
from .auth import get_password_hash

from .auth import authenticate_user, create_access_token
from .schemas import UserAuth, UserData
from .service import get_user_by_id

users_router = APIRouter(prefix='/users', tags=['Users'])


@users_router.post("/login/", summary="Авторизация пользователей")
async def auth_user(response: Response, user_data: UserAuth):
    user = await authenticate_user(email=user_data.email, password=user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Пользователь с такими учетными данными не найден')
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {'access_token': access_token, 'refresh_token': None}


@users_router.get("/{id}", response_model=UserData, summary="Получение данных пользователя")
async def get_user(id: int):
    user = await get_user_by_id(id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Пользователь с id = {id} не найден')
    return {'id': user.id, 'email': user.email, 'full_name': user.full_name}


@users_router.get("/{id}/accounts", response_model=UserData, summary="Получение счетов пользователя")
async def get_user_accounts(id: int):
    user = await get_user_by_id(id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Пользователь с id = {id} не найден')
    return {'id': user.id, 'email': user.email, 'full_name': user.full_name}