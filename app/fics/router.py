from fastapi import APIRouter

from app.auth import get_current_user
from fastapi import  HTTPException, Depends
from starlette import status

from app.fics.models import Fics
from app.fics.py_models import FicSchema, ShowFicSchema, UpdateFicSchema
from app.fics.dao import FicDAO
from app.users.models import Users
from app.fandoms.dao import FandomDAO

router = APIRouter(tags=['Работа с фанфиками'])


@router.get("/fics")
async def get_all_fics():
    fics = await FicDAO.find_all_fics()
    show_fics = [ShowFicSchema.from_orm(fic) for fic in fics]
    print(type(show_fics))
    return show_fics

@router.post("/add_fic")
async def add_fics(
        fic: FicSchema,
        user_data: Users = Depends(get_current_user),
):
    curr_id = user_data.id_user
    fic_dict = fic.dict()
    fic_dict["id_user"] = curr_id
    fandom_title=fic_dict["title_fandom"]
    fandom = await FandomDAO.find_by_title(fandom_title)
    del fic_dict["title_fandom"]
    if fandom is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fandom not found")
    fic_dict["id_fandom"] = fandom.id_fandom
    fic_obj = Fics(**fic_dict)
    result = await FicDAO.create_fic(fic_obj)
    if result:
        return {"message": "Вы успешно добавили фик!!"}

@router.get("/fic")
async def get_fic_by_fandom_id(id_fandom):
    fic = await FicDAO.find_by_id(id_fandom)
    return fic

@router.patch("/fic")
async def update_fic(fic: UpdateFicSchema, user_data: Users = Depends(get_current_user)):
    fic_dict = fic.dict()
    fic_dict["id_user"] = user_data.id_user
    fandom_title = fic_dict["title_fandom"]
    fandom = await FandomDAO.find_by_title(fandom_title)
    del fic_dict["title_fandom"]
    if fandom is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fandom not found")
    fic_dict["id_fandom"] = fandom.id_fandom
    result = await FicDAO.update_fic(**fic_dict)
    return result

@router.delete("/fic")
async def delete_fic(id_fic, user_data: Users = Depends(get_current_user)):
    result = await FicDAO.delete_fic(id_fic, id_user=user_data.id_user)
    if result:
        return {"message": "Вы успешно удалили фик!!"}

@router.post("/fic/like")
async def like_fic(id_fic, user_data: Users = Depends(get_current_user)):
    result = await FicDAO.add_like(id_fic, user_data.id_user)
    if result:
        return {"message": "Вы успешно поставили лайк!!"}

@router.post("/fic/dislike")
async def dislike_fic(id_fic, user_data: Users = Depends(get_current_user)):
    result = await FicDAO.delete_like(id_fic, user_data.id_user)
    if result:
        return {"message": "Вы успешно поставили дизлайк!!"}