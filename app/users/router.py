from fastapi import APIRouter

from app.auth import get_password_hash, authenticate_user, create_access_token, get_current_user
from fastapi import  HTTPException, Depends
from starlette import status
from starlette.responses import Response

from app.users.models import Users
from app.users.py_models import UserSchema, UserResponse
from app.users.dao import UserDAO

router = APIRouter(tags=['Работа с пользователями'])

@router.get("/users", summary="Получить всех пользователей")
async def get_all_users():
    users = await UserDAO.find_all_users()
    return [UserResponse.from_orm(user) for user in users]

@router.post("/register_user/")
async def register_user(
        response: Response, user_data: UserSchema
) -> dict:
    user = await UserDAO.find_by_nickname(user_data.nickname)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Пользователь уже существует"
        )
    user_dict = user_data.dict()
    user_dict["password"] = get_password_hash(user_data.password)
    user_obj = Users(**user_dict)
    result = await UserDAO.create_user(user_obj)
    check = await authenticate_user(login=user_data.nickname, password=user_data.password)
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверная почта или пароль"
        )
    access_token = create_access_token({"sub": str(check.id_user)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {"message": "Вы успешно зарегистрированы!!"}


@router.post("/login_user/")
async def login_user(
        response: Response, user_data: UserSchema
):
    check = await authenticate_user(login=user_data.nickname, password=user_data.password)
    print(check)
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверная почта или пароль"
        )
    access_token = create_access_token({"sub": str(check.id_user)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {"access_token": access_token, "refresh_token": None}


@router.get("/me/")
async def get_me(user_data: Users = Depends(get_current_user)):
    return UserResponse.from_orm(user_data)


@router.post("/logout/")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {"message": "Пользователь успешно вышел из системы"}

@router.patch("/me/", response_model=UserResponse)
async def update_user(user_data: UserSchema, user: Users = Depends(get_current_user)):
    user.nickname = user_data.nickname
    user.password = get_password_hash(user_data.password)
    result = await UserDAO.update_user(user)
    return UserResponse.from_orm(result)