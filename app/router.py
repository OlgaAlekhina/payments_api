from fastapi import APIRouter, HTTPException, status, Response, Depends
from .auth import get_password_hash, get_current_user

from .auth import authenticate_user, create_access_token
from .schemas import UserAuth, UserData, UserAccounts, UserPayments, UserAdd
from .service import get_user_by_id, get_accounts, get_payments, get_user_by_email, add_user

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


@users_router.get("/{id}/accounts", response_model=UserAccounts, summary="Получение счетов пользователя")
async def get_user_accounts(id: int):
    accounts = await get_accounts(id)
    response_data = []
    for account in accounts:
        response_data.append({"id": account.id, "balance": account.balance})
    return {"accounts": response_data}


@users_router.get("/{id}/payments", response_model=UserPayments, summary="Получение платежей пользователя")
async def get_user_payments(id: int):
    payments = await get_payments(id)
    response_data = []
    for payment in payments:
        response_data.append({"payment_id": payment.id, "account_id": payment.account_id, "amount": payment.amount})
    return {"payments": response_data}


@users_router.post("/", summary="Добавление пользователей")
async def create_new_user(user_data: UserAdd):
    user = await get_user_by_email(user_data.email)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Пользователь с такими email уже существует')
    user_dict = user_data.model_dump()
    user_dict['password'] = get_password_hash(user_data.password)
    user_dict['is_user'] = True
    result = await add_user(**user_dict)
    return {'message': 'Пользователь успешно зарегистрирован'}


@users_router.get("/me/")
async def get_me(user_data: UserData = Depends(get_current_user)):
    return user_data