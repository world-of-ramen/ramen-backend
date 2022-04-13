# from typing import Optional
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Path
from starlette.status import HTTP_404_NOT_FOUND

from app.api.dependencies.database import get_repository
from app.db.errors import EntityDoesNotExist
from app.db.repositories.posts import PostsRepository
from app.models.domain.posts import Post
from app.resources import strings


async def get_post_by_id_from_path(
    id: int = Path(...),
    posts_repo: PostsRepository = Depends(get_repository(PostsRepository)),
) -> Post:
    try:
        return await posts_repo.get_post_by_id(id=id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail=strings.POST_DOES_NOT_EXIST_ERROR
        )
