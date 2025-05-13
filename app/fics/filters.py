from typing import Optional

from fastapi_filter.contrib.sqlalchemy import Filter

from app.fics.models import Fics

class FicFilter(Filter):
    title__ilike: Optional[str] = None
    description__ilike: Optional[str] = None
    likes__ge: Optional[int] = None     # минимум
    likes__le: Optional[int] = None     # максимум

    class Constants(Filter.Constants):
        model = Fics