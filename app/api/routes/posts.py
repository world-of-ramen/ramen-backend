from typing import Optional

from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from fastapi import Query

from app.api.dependencies.database import get_repository
from app.api.dependencies.posts import get_post_by_id_from_path
from app.db.repositories.posts import PostsRepository
from app.models.domain.posts import Post
from app.models.schemas.posts import PostInCreate
from app.models.schemas.posts import PostInResponse
from app.models.schemas.posts import PostInUpdate
from app.models.schemas.posts import PostListResponse
from app.resources import status


router = APIRouter()


@router.get("/list", response_model=PostListResponse, name="post:get-post-list")
async def retrieve_post_list(
    store_id: Optional[int] = Query(None, ge=1),
    user_id: Optional[int] = Query(None, ge=1),
    limit: int = Query(100, ge=1),
    offset: int = Query(0, ge=0),
    posts_repo: PostsRepository = Depends(get_repository(PostsRepository)),
) -> PostListResponse:
    posts = await posts_repo.get_post_list(
        limit=limit, offset=offset, store_id=store_id, user_id=user_id
    )

    return posts


@router.get("/{id}", response_model=PostInResponse, name="post:get-post-by-id")
async def retrieve_post(
    # staff: Staff = Depends(get_current_staff_authorizer()),
    post_in_db: Post = Depends(get_post_by_id_from_path),
) -> PostInResponse:
    return PostInResponse(post=post_in_db)


@router.post("", response_model=PostInResponse, name="post:create-post")
async def create_post(
    # staff: Staff = Depends(get_current_staff_authorizer()),
    post_create: PostInCreate = Body(..., embed=True, alias="post"),
    posts_repo: PostsRepository = Depends(get_repository(PostsRepository)),
) -> PostInResponse:
    post_created = await posts_repo.create_new_post(**post_create.dict())

    return PostInResponse(post=post_created)


@router.put("/{id}", response_model=PostInResponse, name="post:update-post-by-id")
async def update_post(
    # staff: Staff = Depends(get_current_staff_authorizer()),
    post_update: PostInUpdate = Body(..., embed=True, alias="post"),
    post_in_db: Post = Depends(get_post_by_id_from_path),
    posts_repo: PostsRepository = Depends(get_repository(PostsRepository)),
) -> PostInResponse:
    post_updated = await posts_repo.update_post(
        post_in_db=post_in_db, **post_update.dict()
    )

    return PostInResponse(post=post_updated)


@router.delete(
    "/{id}",
    response_model=PostInResponse,
    name="posts:update-post-stautus-deleted-by-id",
)
async def delete_post(
    # staff: Staff = Depends(get_current_staff_authorizer()),
    post_in_db: Post = Depends(get_post_by_id_from_path),
    posts_repo: PostsRepository = Depends(get_repository(PostsRepository)),
) -> PostInResponse:

    post_updated = await posts_repo.update_post(
        post_in_db=post_in_db, status=status.DELETED
    )

    return PostInResponse(post=post_updated)
