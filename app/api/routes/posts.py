from typing import Optional

from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Query
from starlette.status import HTTP_401_UNAUTHORIZED
from starlette.status import HTTP_403_FORBIDDEN

from app.api.dependencies.authentication import get_current_user_authorizer
from app.api.dependencies.database import get_repository
from app.api.dependencies.posts import get_post_by_id_from_path
from app.db.repositories.posts import PostsRepository
from app.models.domain.posts import Post
from app.models.domain.users import User
from app.models.schemas.posts import PostInCreate
from app.models.schemas.posts import PostInResponse
from app.models.schemas.posts import PostInUpdate
from app.models.schemas.posts import PostListResponse
from app.resources import status
from app.resources import strings

router = APIRouter()


@router.get(
    "/list",
    response_model=PostListResponse,
    name="post:get-post-list",
    description="有帶store_id則會回傳該store的post, 沒帶則會回傳該用戶的post",
)
async def retrieve_post_list(
    user: User = Depends(get_current_user_authorizer(required=False)),
    store_id: Optional[int] = Query(None, ge=1),
    limit: int = Query(100, ge=1),
    offset: int = Query(0, ge=0),
    posts_repo: PostsRepository = Depends(get_repository(PostsRepository)),
) -> PostListResponse:
    print(f"user: {user}")
    if not user and not store_id:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail=strings.AUTHENTICATION_REQUIRED
        )

    posts = await posts_repo.get_post_list(
        limit=limit,
        offset=offset,
        store_id=store_id,
        user_id=user.id_ if user else None,
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
    user: User = Depends(get_current_user_authorizer()),
    post_create: PostInCreate = Body(..., embed=True, alias="post"),
    posts_repo: PostsRepository = Depends(get_repository(PostsRepository)),
) -> PostInResponse:
    post_created = await posts_repo.create_new_post(
        **post_create.dict(), user_id=user.id_
    )

    return PostInResponse(post=post_created)


@router.put("/{id}", response_model=PostInResponse, name="post:update-post-by-id")
async def update_post(
    user: User = Depends(get_current_user_authorizer()),
    post_update: PostInUpdate = Body(..., embed=True, alias="post"),
    post_in_db: Post = Depends(get_post_by_id_from_path),
    posts_repo: PostsRepository = Depends(get_repository(PostsRepository)),
) -> PostInResponse:
    if user.id_ != post_in_db.user_id:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail=strings.USER_IS_NOT_AUTHOR_OF_POST
        )

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
