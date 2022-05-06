from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Path
from fastapi import Query
from starlette.status import HTTP_403_FORBIDDEN

from app.api.dependencies.authentication import get_current_user_authorizer
from app.api.dependencies.database import get_repository
from app.api.dependencies.stores import get_store_by_id_from_path
from app.core.config import get_app_settings
from app.db.repositories.stores import StoresRepository
from app.models.domain.google import PlaceInfo
from app.models.domain.stores import Store
from app.models.domain.users import User
from app.models.schemas.stores import StoreInCreate
from app.models.schemas.stores import StoreInResponse
from app.models.schemas.stores import StoreInUpdate
from app.models.schemas.stores import StoreListResponse
from app.resources import status
from app.resources import strings

SETTINGS = get_app_settings()
router = APIRouter()


@router.get("/list", response_model=StoreListResponse, name="store:get-store-list")
async def retrieve_store_list(
    limit: int = Query(100, ge=1),
    offset: int = Query(0, ge=0),
    with_posts: int = Query(1, ge=0),
    stores_repo: StoresRepository = Depends(get_repository(StoresRepository)),
) -> StoreListResponse:
    stores = await stores_repo.get_store_list(
        limit=limit, offset=offset, with_posts=with_posts
    )

    return stores


@router.get(
    "/place_id/{name}",
    response_model=PlaceInfo,
    name="store:get-google-place-id-by-store-id",
)
async def retrieve_place_id_by_store_id(
    name: str = Path(..., description="店名：例：麵屋吉光"),
    stores_repo: StoresRepository = Depends(get_repository(StoresRepository)),
) -> PlaceInfo:
    place_info = await stores_repo._get_google_place_id_by_name(name=name)
    return place_info


@router.get("/{id}", response_model=StoreInResponse, name="store:get-store-by-id")
async def retrieve_store(
    store_in_db: Store = Depends(get_store_by_id_from_path),
) -> StoreInResponse:
    return StoreInResponse(store=store_in_db)


@router.post("", response_model=StoreInResponse, name="store:create-store")
async def create_store(
    user: User = Depends(get_current_user_authorizer()),
    store_create: StoreInCreate = Body(..., embed=True, alias="store"),
    stores_repo: StoresRepository = Depends(get_repository(StoresRepository)),
) -> StoreInResponse:
    admin_list = SETTINGS.admin_wallet_address
    if user.wallet_address not in admin_list:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail=strings.NOT_AUTHORIZED
        )
    store_created = await stores_repo.create_new_store(**store_create.dict())

    return StoreInResponse(store=store_created)


@router.put("/{id}", response_model=StoreInResponse, name="stores:update-store-by-id")
async def update_store(
    user: User = Depends(get_current_user_authorizer()),
    store_update: StoreInUpdate = Body(..., embed=True, alias="store"),
    store_in_db: Store = Depends(get_store_by_id_from_path),
    stores_repo: StoresRepository = Depends(get_repository(StoresRepository)),
) -> StoreInResponse:
    admin_list = SETTINGS.admin_wallet_address
    if user.wallet_address not in admin_list:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail=strings.NOT_AUTHORIZED
        )
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
    user: User = Depends(get_current_user_authorizer()),
    store_in_db: Store = Depends(get_store_by_id_from_path),
    stores_repo: StoresRepository = Depends(get_repository(StoresRepository)),
) -> StoreInResponse:
    admin_list = SETTINGS.admin_wallet_address
    if user.wallet_address not in admin_list:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail=strings.NOT_AUTHORIZED
        )
    store_updated = await stores_repo.update_store(
        store_in_db=store_in_db, status=status.DELETED
    )

    return StoreInResponse(store=store_updated)
