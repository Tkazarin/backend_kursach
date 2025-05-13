from typing import Optional

from fastapi_filter.contrib.sqlalchemy import Filter

from app.fandoms.models import Fandoms

class FandomFilter(Filter):
    title__ilike: Optional[str] = None
    type: Optional[str] = None

    class Constants(Filter.Constants):
        model = Fandoms