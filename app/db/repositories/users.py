from typing import Optional

from app.db.errors import EntityDoesNotExist
from app.db.queries.queries import queries
from app.db.repositories.base import BaseRepository
from app.models.domain.users import User


class UsersRepository(BaseRepository):
    async def get_user_by_id(self, *, id: int) -> User:
        user_row = await queries.get_user_by_id(self.connection, id=id)
        if user_row:
            return User(**user_row)

        raise EntityDoesNotExist(f"user with id {id} does not exist")

    async def get_user_by_wallet_address(self, *, wallet_address: str) -> Optional[User]:
        user_row = await queries.get_user_by_wallet_address(
            self.connection, wallet_address=wallet_address
        )
        if user_row:
            return User(**user_row)
        else:
            return None

    async def create_user(
        self, *, wallet_address: str, image: Optional[str] = None
    ) -> User:
        user = User(wallet_address=wallet_address, image=image, status=1)

        async with self.connection.transaction():
            user_row = await queries.create_new_user(
                self.connection,
                wallet_address=user.wallet_address,
                image=user.image,
                status=user.status,
            )
            user.id_ = user_row["id"]
        return user.copy(update=dict(user_row))

    async def update_user(
        self,
        *,
        user: User,
        wallet_address: Optional[str] = None,
        image: Optional[str] = None,
        status: Optional[int] = None,
    ) -> User:
        user_in_db = await self.get_user_by_id(id=user.id_)
        user_in_db.wallet_address = wallet_address or user_in_db.wallet_address
        user_in_db.image = image or user_in_db.image
        user_in_db.status = status if status is not None else user_in_db.status

        async with self.connection.transaction():
            user_in_db.updated_at = await queries.update_user_by_id(
                self.connection,
                id=user.id_,
                new_wallet_address=user.wallet_address,
                new_image=user_in_db.image,
                new_status=user_in_db.status,
            )

        return user_in_db
