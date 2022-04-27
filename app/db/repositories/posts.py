from typing import Optional

from asyncpg import Connection
from asyncpg import Record

from app.core.config import get_app_settings
from app.db.errors import EntityDoesNotExist
from app.db.queries.queries import queries
from app.db.repositories.base import BaseRepository
from app.db.repositories.comments import CommentsRepository
from app.db.repositories.users import UsersRepository
from app.models.domain.posts import Post
from app.models.domain.posts import PostWithComments
from app.models.domain.posts import PostWithWalletAddress
from app.models.schemas.posts import PostListResponse

SETTINGS = get_app_settings()


class PostsRepository(BaseRepository):
    def __init__(self, conn: Connection) -> None:
        super().__init__(conn)
        self._users_repo = UsersRepository(conn)
        self._comments_repo = CommentsRepository(conn)

    async def get_post_by_id(self, *, id: int) -> PostWithWalletAddress:
        post_row = await queries.get_post_by_id(self.connection, id=id)

        if post_row:
            return await self._get_post_from_db_record(post_row=post_row)

        raise EntityDoesNotExist(f"post with id {id} does not exist")

    async def get_post_list(
        self,
        *,
        limit: int = 100,
        comments_limit: int = 3,
        offset: int = 0,
        store_id: Optional[int] = None,
        user_id: Optional[int] = None,
        is_public: Optional[bool] = None,
    ) -> PostListResponse:
        if store_id is not None:
            post_rows = await queries.get_posts_by_store_id(
                self.connection, limit=limit, offset=offset, store_id=store_id
            )
        elif is_public:
            post_rows = await queries.get_latest_posts(
                self.connection, limit=limit, offset=offset
            )
        else:
            post_rows = await queries.get_posts_by_user_id(
                self.connection, limit=limit, offset=offset, user_id=user_id
            )

        total = (
            await self._get_post_list_total_from_db_record(post_row=post_rows[0])
            if post_rows
            else 0
        )

        post_list = [
            await self._get_post_from_db_for_list_record(
                post_row=post_row, comments_limit=comments_limit
            )
            for post_row in post_rows
        ]

        return PostListResponse(posts=post_list, total=total)

    async def _get_post_from_db_record(
        self, *, post_row: Record
    ) -> PostWithWalletAddress:
        user_id = post_row["user_id"]
        user_wallet_address = (
            await self._users_repo.get_wallet_address_by_user_id(user_id=user_id)
            if user_id is not None
            else "匿名"
        )

        return PostWithWalletAddress(
            id_=post_row["id"],
            store_id=post_row["store_id"],
            user_id=user_id,
            user_wallet_address=user_wallet_address,
            body=post_row["body"],
            image_url=post_row["image_url"],
            rating=post_row["rating"],
            status=post_row["status"],
            created_at=post_row["created_at"],
            updated_at=post_row["updated_at"],
        )

    async def _get_post_from_db_for_list_record(
        self, *, post_row: Record, comments_limit: int
    ) -> PostWithComments:
        user_id = post_row["user_id"]
        post_id = post_row["id"]

        user_wallet_address = (
            await self._users_repo.get_wallet_address_by_user_id(user_id=user_id)
            if user_id is not None
            else "匿名"
        )

        comments = await self._comments_repo.get_comment_list(
            post_id=post_id, limit=comments_limit
        )

        return PostWithComments(
            id_=post_id,
            store_id=post_row["store_id"],
            user_id=user_id,
            user_wallet_address=user_wallet_address,
            body=post_row["body"],
            image_url=post_row["image_url"],
            rating=post_row["rating"],
            comments=comments.comments,
            status=post_row["status"],
            created_at=post_row["created_at"],
            updated_at=post_row["updated_at"],
        )

    async def _get_post_list_total_from_db_record(self, *, post_row: Record) -> int:
        return post_row["total"]

    async def create_new_post(
        self,
        *,
        store_id: int,
        user_id: int,
        body: Optional[str] = None,
        image_url: Optional[str] = None,
        rating: Optional[float] = None,
        status: int = 1,
    ) -> Post:
        new_post = Post(
            store_id=store_id,
            user_id=user_id,
            body=body,
            image_url=image_url,
            rating=rating,
            status=status,
        )

        async with self.connection.transaction():
            post_row = await queries.create_post(
                self.connection,
                store_id=store_id,
                user_id=user_id,
                body=body,
                image_url=image_url,
                rating=rating,
                status=status,
            )

        return new_post.copy(update=dict(post_row))

    async def update_post(
        self,
        *,
        post_in_db: PostWithWalletAddress,
        body: Optional[str] = None,
        image_url: Optional[str] = None,
        rating: Optional[float] = None,
        status: Optional[int] = None,
    ) -> PostWithWalletAddress:
        post_in_db.body = body or post_in_db.body
        post_in_db.image_url = image_url or post_in_db.image_url
        post_in_db.rating = rating if rating is not None else post_in_db.rating
        post_in_db.status = status if status is not None else post_in_db.status

        async with self.connection.transaction():
            post_in_db.updated_at = await queries.update_post_by_id(
                self.connection,
                id=post_in_db.id_,
                new_body=post_in_db.body,
                new_image_url=post_in_db.image_url,
                new_rating=post_in_db.rating,
                new_status=post_in_db.status,
            )

        return post_in_db
