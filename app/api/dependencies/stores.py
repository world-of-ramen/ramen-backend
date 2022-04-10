# from typing import Optional
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Path
from starlette.status import HTTP_404_NOT_FOUND

from app.api.dependencies.database import get_repository
from app.db.errors import EntityDoesNotExist
from app.db.repositories.stores import StoresRepository
from app.models.domain.stores import Store
from app.resources import strings


async def get_store_by_id_from_path(
    id: int = Path(...),
    stores_repo: StoresRepository = Depends(get_repository(StoresRepository)),
) -> Store:
    try:
        return await stores_repo.get_store_by_id(id=id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail=strings.STORE_DOES_NOT_EXIST_ERROR
        )
