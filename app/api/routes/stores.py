from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from fastapi import Path
from fastapi import Query

from app.api.dependencies.database import get_repository
from app.api.dependencies.stores import get_store_by_id_from_path
from app.db.repositories.stores import StoresRepository
from app.models.domain.google import PlaceId
from app.models.domain.stores import Store
from app.models.schemas.stores import StoreInCreate
from app.models.schemas.stores import StoreInResponse
from app.models.schemas.stores import StoreInUpdate
from app.models.schemas.stores import StoreListResponse
from app.resources import status


router = APIRouter()


@router.get("/list", response_model=StoreListResponse, name="store:get-store-list")
async def retrieve_store_list(
    limit: int = Query(100, ge=1),
    offset: int = Query(0, ge=0),
    stores_repo: StoresRepository = Depends(get_repository(StoresRepository)),
) -> StoreListResponse:
    stores = await stores_repo.get_store_list(limit=limit, offset=offset)

    return stores


@router.get(
    "/place_id/{name}",
    response_model=PlaceId,
    name="store:get-google-place-id-by-store-id",
)
async def retrieve_place_id_by_store_id(
    # staff: Staff = Depends(get_current_staff_authorizer()),
    name: str = Path(..., description="店名：例：麵屋吉光"),
    stores_repo: StoresRepository = Depends(get_repository(StoresRepository)),
) -> PlaceId:
    place_id = await stores_repo._get_google_place_id_by_name(name=name)
    return place_id


@router.get("/{id}", response_model=StoreInResponse, name="store:get-store-by-id")
async def retrieve_store(
    # staff: Staff = Depends(get_current_staff_authorizer()),
    store_in_db: Store = Depends(get_store_by_id_from_path),
) -> StoreInResponse:
    return StoreInResponse(store=store_in_db)


@router.post("", response_model=StoreInResponse, name="store:create-store")
async def create_store(
    # staff: Staff = Depends(get_current_staff_authorizer()),
    store_create: StoreInCreate = Body(..., embed=True, alias="store"),
    stores_repo: StoresRepository = Depends(get_repository(StoresRepository)),
) -> StoreInResponse:
    store_created = await stores_repo.create_new_store(**store_create.dict())

    return StoreInResponse(store=store_created)


@router.put("/{id}", response_model=StoreInResponse, name="stores:update-store-by-id")
async def update_store(
    # staff: Staff = Depends(get_current_staff_authorizer()),
    store_update: StoreInUpdate = Body(..., embed=True, alias="store"),
    store_in_db: Store = Depends(get_store_by_id_from_path),
    stores_repo: StoresRepository = Depends(get_repository(StoresRepository)),
) -> StoreInResponse:
    store_updated = await stores_repo.update_store(
        store_in_db=store_in_db, **store_update.dict()
    )

    return StoreInResponse(store=store_updated)


@router.delete(
    "/{id}",
    response_model=StoreInResponse,
    name="stores:update-store-stautus-deleted-by-id",
)
async def delete_store(
    # staff: Staff = Depends(get_current_staff_authorizer()),
    store_in_db: Store = Depends(get_store_by_id_from_path),
    stores_repo: StoresRepository = Depends(get_repository(StoresRepository)),
) -> StoreInResponse:

    store_updated = await stores_repo.update_store(
        store_in_db=store_in_db, status=status.DELETED
    )

    return StoreInResponse(store=store_updated)
