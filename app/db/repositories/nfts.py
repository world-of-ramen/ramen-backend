from typing import List

from asyncpg import Record

from app.db.errors import EntityDoesNotExist
from app.db.queries.queries import queries
from app.db.repositories.base import BaseRepository
from app.models.domain.nfts import NFT
from app.models.schemas.nfts import NFTListResponse


class NFTsRepository(BaseRepository):
    async def get_nft_by_id(self, *, id: int) -> NFT:
        row = await queries.get_nft_by_id(self.connection, id=id)
        if row:
            return NFT(**row)

        raise EntityDoesNotExist(f"nft with id {id} does not exist")

    async def get_nfts_by_user_id(self, *, user_id: int) -> NFTListResponse:
        rows = await queries.get_nfts_by_user_id(self.connection, user_id=user_id)

        nfts = [await self._get_nft_from_db_record(row=row) for row in rows]

        return NFTListResponse(nfts=nfts)

    async def _get_nft_from_db_record(self, *, row: Record) -> NFT:
        return NFT(
            id_=row["id"],
            user_id=row["user_id"],
            wallet_address=row["wallet_address"],
            image_url=row["image_url"],
            token_address=row["token_address"],
            token_id=row["token_id"],
            name=row["name"],
            symbol=row["symbol"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    async def get_nft(
        self, *, user_id: int, wallet_address: str, token_address: str, token_id: int
    ) -> NFT:
        row = await queries.get_nft(
            self.connection,
            user_id=user_id,
            wallet_address=wallet_address,
            token_address=token_address,
            token_id=token_id,
        )
        if row:
            return NFT(**row)

        raise EntityDoesNotExist(
            f"nft with (user_id {user_id}, wallet_address {wallet_address}, token_address {token_address}, token_id {token_id}) does not exist"
        )

    async def create_nft(
        self,
        *,
        user_id: int,
        wallet_address: str,
        image_url: str,
        token_address: str,
        token_id: int,
        name: str,
        symbol: str,
    ) -> NFT:
        nft = NFT(
            user_id=user_id,
            wallet_address=wallet_address,
            image_url=image_url,
            token_address=token_address,
            token_id=token_id,
            name=name,
            symbol=symbol,
        )

        async with self.connection.transaction():
            row = await queries.create_new_nft(
                self.connection,
                user_id=user_id,
                wallet_address=wallet_address,
                image_url=image_url,
                token_address=token_address,
                token_id=token_id,
                name=name,
                symbol=symbol,
            )
            nft.id_ = row["id"]
        return nft.copy(update=dict(row))

    async def update_nft(self, *, id: int, image_url: str) -> NFT:
        nft_in_db = await self.get_nft_by_id(id=id)
        nft_in_db.image_url = image_url or nft_in_db.image_url
        async with self.connection.transaction():
            nft_in_db.updated_at = await queries.update_nft_by_id(
                self.connection,
                id=id,
                new_image_url=nft_in_db.image_url,
            )

        return nft_in_db

    async def get_whitelist_contract(self, *, id: int) -> List[str]:
        rows = await queries.get_whitelist_contract(self.connection)
        list = []
        for row in rows:
            list.append[row]
