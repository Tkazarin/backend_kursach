from fastapi import APIRouter

from app.auth import get_current_user, get_current_admin_user
from fastapi import  HTTPException, Depends
from starlette import status
from starlette.responses import Response

from app.fandoms.models import Fandoms
from app.fandoms.py_models import FandomSchema
from app.fandoms.dao import FandomDAO
from app.users.models import Users

router = APIRouter(tags=['Работа с фандомами'])


@router.get("/fandoms")
async def get_all_fandoms():
    fandoms = await FandomDAO.find_all_fandoms()
    return [fandom for fandom in fandoms]

@router.post("/add_fandom")
async def add_fandom(
        fandom: FandomSchema,
        user_data: Users = Depends(get_current_admin_user),
):
    fandom_dict = fandom.dict()
    fandom_obj = Fandoms(**fandom_dict)
    result = await FandomDAO.create_fandom(fandom_obj)
    if result:
        return {"message": "Вы успешно добавили фандом!!"}

@router.get("/fandom")
async def get_fandom_by_id(id_fandom):
    fandom = await FandomDAO.find_by_id(id_fandom)
    return fandom

@router.patch("/fandom")
async def update_fandom(fandom: FandomSchema, user_data: Users = Depends(get_current_admin_user)):
    fandom = Fandoms(**fandom.dict())
    result = await FandomDAO.update_fandom(fandom)
    return fandom

@router.delete("/fandom")
async def delete_fandom(id_fandom, user_data: Users = Depends(get_current_admin_user)):
    result = await FandomDAO.delete_fandom(id_fandom)
    if result:
        return {"message": "Вы успешно удалили фандом!!"}