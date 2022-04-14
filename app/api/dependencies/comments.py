# from typing import Optional
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Path
from starlette.status import HTTP_404_NOT_FOUND

from app.api.dependencies.database import get_repository
from app.db.errors import EntityDoesNotExist
from app.db.repositories.comments import CommentsRepository
from app.models.domain.comments import CommentWithWalletAddress
from app.resources import strings


async def get_comment_by_id_from_path(
    id: int = Path(...),
    comments_repo: CommentsRepository = Depends(get_repository(CommentsRepository)),
) -> CommentWithWalletAddress:
    try:
        return await comments_repo.get_comment_by_id(id=id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail=strings.COMMENT_DOES_NOT_EXIST_ERROR
        )
