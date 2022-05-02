from typing import Optional

from asyncpg import Connection
from asyncpg import Record

from app.core.config import get_app_settings
from app.db.errors import EntityDoesNotExist
from app.db.queries.queries import queries
from app.db.repositories.base import BaseRepository
from app.db.repositories.users import UsersRepository
from app.models.domain.comments import Comment
from app.models.domain.comments import CommentWithWalletAddress
from app.models.schemas.comments import CommentListResponse

SETTINGS = get_app_settings()


class CommentsRepository(BaseRepository):
    def __init__(self, conn: Connection) -> None:
        super().__init__(conn)
        self._users_repo = UsersRepository(conn)

    async def get_comment_by_id(self, *, id: int) -> CommentWithWalletAddress:
        comment_row = await queries.get_comment_by_id(self.connection, id=id)

        if comment_row:
            return await self._get_comment_from_db_record(comment_row=comment_row)

        raise EntityDoesNotExist(f"comment with id {id} does not exist")

    async def get_comment_list(
        self,
        *,
        post_id: int,
        limit: int = 100,
        offset: int = 0,
    ) -> CommentListResponse:
        comment_rows = await queries.get_comments_by_post_id(
            self.connection, limit=limit, offset=offset, post_id=post_id
        )

        total = (
            await self._get_comment_list_total_from_db_record(
                comment_row=comment_rows[0]
            )
            if comment_rows
            else 0
        )

        comment_list = [
            await self._get_comment_from_db_record(comment_row=comment_row)
            for comment_row in comment_rows
        ]

        return CommentListResponse(comments=comment_list, total=total)

    async def _get_comment_from_db_record(
        self, *, comment_row: Record
    ) -> CommentWithWalletAddress:
        user_id = comment_row["user_id"]
        user_info = (
            await self._users_repo.get_user_by_id(id=user_id)
            if user_id is not None
            else None
        )

        return CommentWithWalletAddress(
            id_=comment_row["id"],
            post_id=comment_row["post_id"],
            user_id=user_id,
            user_wallet_address=user_info.wallet_address
            if user_info and user_info.wallet_address is not None
            else "訪客",
            user_image=user_info.image if user_info else None,
            body=comment_row["body"],
            status=comment_row["status"],
            created_at=comment_row["created_at"],
            updated_at=comment_row["updated_at"],
        )

    async def _get_comment_list_total_from_db_record(
        self, *, comment_row: Record
    ) -> int:
        return comment_row["total"]

    async def create_new_comment(
        self,
        *,
        post_id: int,
        user_id: Optional[int] = None,
        body: Optional[str] = None,
        status: int = 1,
    ) -> Comment:
        new_comment = Comment(
            post_id=post_id,
            user_id=user_id,
            body=body,
            status=status,
        )

        async with self.connection.transaction():
            comment_row = await queries.create_comment(
                self.connection,
                post_id=post_id,
                user_id=user_id,
                body=body,
                status=status,
            )

        return new_comment.copy(update=dict(comment_row))

    async def update_comment(
        self,
        *,
        comment_in_db: CommentWithWalletAddress,
        body: Optional[str] = None,
        status: Optional[int] = None,
    ) -> CommentWithWalletAddress:
        comment_in_db.body = body or comment_in_db.body
        comment_in_db.status = status if status is not None else comment_in_db.status

        async with self.connection.transaction():
            comment_in_db.updated_at = await queries.update_comment_by_id(
                self.connection,
                id=comment_in_db.id_,
                new_body=comment_in_db.body,
                new_status=comment_in_db.status,
            )

        return comment_in_db
