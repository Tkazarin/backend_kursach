from fastapi import APIRouter
from fastapi.params import Query, Path
from fastapi_filter import FilterDepends, with_prefix
from fastapi_pagination import Page, Params, paginate


from app.auth import get_current_user
from fastapi import  HTTPException, Depends
from starlette import status
from starlette.responses import Response

from app.comments.models import Comments
from app.comments.py_models import ShowCommentSchema
from app.comments.dao import CommentDAO
from app.fics.filters import FicFilter

from app.users.models import Users
from app.users.py_models import UserResponse
from app.users.dao import UserDAO

from app.fics.models import Fics
from app.fics.py_models import ShowFicSchema
from app.fics.dao import FicDAO

from app.fandoms.models import Fandoms
from app.fandoms.py_models import FandomSchema
from app.fandoms.dao import FandomDAO
from app.fandoms.filters import FandomFilter

router = APIRouter(tags=['Работа с выдачей информации для страниц'])

@router.get("/my_mirror/")
async def get_my_mirror(
    user_data: Users = Depends(get_current_user),
    page: int = Query(1, ge=1, description="Номер страницы"),
    page_size: int = Query(10, ge=1, le=50, description="Размер страницы"),
):
    user_info = UserResponse.from_orm(user_data)

    fics_list = await FicDAO.find_by_user(
        id_user=user_data.id_user,
        offset=(page-1)*page_size,
        limit=page_size,
    )
    show_fics = [ShowFicSchema.from_orm(fic) for fic in fics_list]

    return {
        "user_info": user_info,
        "fics": show_fics,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "fics_count": len(show_fics)
        }
    }

@router.get("/mirror_gazing/")
async def mirror_gazing():
    fandoms = await FandomDAO.get_random_fandoms(3)
    show_fandoms = [FandomSchema.from_orm(f) for f in fandoms]

    popular_fics = await FicDAO.get_top_fics(3)
    show_popular_fics = [ShowFicSchema.from_orm(fic) for fic in popular_fics]

    return {
        "random_fandoms": show_fandoms,
        "popular_fics": show_popular_fics,
    }
@router.get("/mirror_worlds/", response_model=Page[FandomSchema])
async def get_fandoms(
    fandom_filter: FandomFilter = FilterDepends(FandomFilter),
    params: Params = Depends(),
):
    fandoms = await FandomDAO.find_filtered_fandoms(fandom_filter)
    schemas = [FandomSchema.from_orm(fandom) for fandom in fandoms]
    return paginate(schemas, params)


@router.get("/shard/{fic_title}/", response_model=dict)
async def get_fic_and_comments(
        fic_title: str = Path(..., description="Название фанфика"),
        params: Params = Depends()
):
    fic = await FicDAO.find_by_title(fic_title)
    if not fic:
        raise HTTPException(status_code=404, detail="Фанфик не найден")
    show_fic = ShowFicSchema.from_orm(fic)

    comments = await CommentDAO.find_by_fic(fic.id_fic)
    show_comms = [ShowCommentSchema.from_orm(comm) for comm in comments]
    paginated_comments = paginate(show_comms, params)

    return {
        "fic": show_fic,
        "comments": paginated_comments
    }

@router.get("/mirror_worlds/{id_fandom}/")
async def mirror_worlds_page(
    id_fandom: int,
    params: Params = Depends(),
    fics_filter: FicFilter = FilterDepends(with_prefix("fic", FicFilter)),
):
    fandom = await FandomDAO.find_by_id(id_fandom)
    if not fandom:
        raise HTTPException(status_code=404, detail="Фандом не найден")
    def filter_query(query):
        query = query.where(Fics.id_fandom == id_fandom)
        return fics_filter.filter(query) if fics_filter else query
    fics = await FicDAO.find_all_filtered_fics(filter_query)
    show_fics = [ShowFicSchema.from_orm(fic) for fic in fics]
    page = paginate(show_fics, params)

    return {
        "fandom": FandomSchema.from_orm(fandom),
        "fics": page
    }
