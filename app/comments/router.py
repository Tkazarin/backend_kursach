from fastapi import APIRouter

from app.auth import get_current_user
from fastapi import Depends

from app.comments.models import Comments
from app.comments.py_models import CommentSchema, ShowCommentSchema, UpdateCommentSchema
from app.comments.dao import CommentDAO
from app.users.models import Users

router = APIRouter(tags=['Работа с комментариями'])


@router.get("/comms")
async def get_all_comments(id_fic):
    comments = await CommentDAO.find_by_fic(id_fic)
    show_comms = [ShowCommentSchema.from_orm(comm) for comm in comments]
    return show_comms

@router.post("/add_comm")
async def add_comms(
        comm: CommentSchema,
        user_data: Users = Depends(get_current_user),
):
    curr_id = user_data.id_user
    comm_dict = comm.dict()
    comm_dict["id_user"] = curr_id
    comm_obj = Comments(**comm_dict)
    result = await CommentDAO.create_comment(comm_obj)
    if result:
        return {"message": "Вы успешно добавили комментарий!!"}

@router.get("/comm")
async def get_comm_by_id(id_comment):
    comm = await CommentDAO.find_by_id(id_comment)
    return comm

@router.patch("/comm")
async def update_fic(comm: UpdateCommentSchema, user_data: Users = Depends(get_current_user)):
    comm_dict = comm.dict()
    comm_dict["id_user"] = user_data.id_user
    result = await CommentDAO.update_comment(**comm_dict)
    return result

@router.delete("/comm")
async def delete_fic(id_comment, user_data: Users = Depends(get_current_user)):
    result = await CommentDAO.delete_comment(id_comment, id_user=user_data.id_user)
    if result:
        return {"message": "Вы успешно удалили фик!!"}