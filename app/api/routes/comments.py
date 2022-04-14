from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Query
from starlette.status import HTTP_403_FORBIDDEN

from app.api.dependencies.authentication import get_current_user_authorizer
from app.api.dependencies.comments import get_comment_by_id_from_path
from app.api.dependencies.database import get_repository
from app.db.repositories.comments import CommentsRepository
from app.models.domain.comments import Comment
from app.models.domain.users import User
from app.models.schemas.comments import CommentInCreate
from app.models.schemas.comments import CommentInResponse
from app.models.schemas.comments import CommentInUpdate
from app.models.schemas.comments import CommentListResponse
from app.resources import status
from app.resources import strings

router = APIRouter()


@router.get(
    "/list",
    response_model=CommentListResponse,
    name="comment:get-comment-list",
    description="",
)
async def retrieve_comment_list(
    post_id: int = Query(...),
    limit: int = Query(100, ge=1),
    offset: int = Query(0, ge=0),
    comments_repo: CommentsRepository = Depends(get_repository(CommentsRepository)),
) -> CommentListResponse:

    comments = await comments_repo.get_comment_list(
        limit=limit,
        offset=offset,
        post_id=post_id,
    )

    return comments


@router.get("/{id}", response_model=CommentInResponse, name="comment:get-comment-by-id")
async def retrieve_comment(
    comment_in_db: Comment = Depends(get_comment_by_id_from_path),
) -> CommentInResponse:
    return CommentInResponse(comment=comment_in_db)


@router.post("", response_model=CommentInResponse, name="comment:create-comment")
async def create_comment(
    user: User = Depends(get_current_user_authorizer(required=False)),
    comment_create: CommentInCreate = Body(..., embed=True, alias="comment"),
    comments_repo: CommentsRepository = Depends(get_repository(CommentsRepository)),
) -> CommentInResponse:
    comment_created = await comments_repo.create_new_comment(
        **comment_create.dict(), user_id=user.id_ if user else None
    )

    return CommentInResponse(comment=comment_created)


@router.put(
    "/{id}", response_model=CommentInResponse, name="comment:update-comment-by-id"
)
async def update_comment(
    user: User = Depends(get_current_user_authorizer()),
    comment_update: CommentInUpdate = Body(..., embed=True, alias="comment"),
    comment_in_db: Comment = Depends(get_comment_by_id_from_path),
    comments_repo: CommentsRepository = Depends(get_repository(CommentsRepository)),
) -> CommentInResponse:
    if user.id_ != comment_in_db.user_id:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail=strings.USER_IS_NOT_AUTHOR_OF_COMMENT
        )

    comment_updated = await comments_repo.update_comment(
        comment_in_db=comment_in_db, **comment_update.dict()
    )

    return CommentInResponse(comment=comment_updated)


@router.delete(
    "/{id}",
    response_model=CommentInResponse,
    name="comments:update-comment-stautus-deleted-by-id",
)
async def delete_comment(
    user: User = Depends(get_current_user_authorizer()),
    comment_in_db: Comment = Depends(get_comment_by_id_from_path),
    comments_repo: CommentsRepository = Depends(get_repository(CommentsRepository)),
) -> CommentInResponse:
    if user.id_ != comment_in_db.user_id:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail=strings.USER_IS_NOT_AUTHOR_OF_COMMENT
        )

    comment_updated = await comments_repo.update_comment(
        comment_in_db=comment_in_db, status=status.DELETED
    )

    return CommentInResponse(comment=comment_updated)
