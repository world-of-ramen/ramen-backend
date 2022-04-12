from app.db.errors import EntityDoesNotExist
from app.db.queries.queries import queries
from app.db.repositories.base import BaseRepository
from app.models.domain.nfts import NFT


class NFTsRepository(BaseRepository):
    async def get_nft_by_id(self, *, id: int) -> NFT:
        row = await queries.get_nft_by_id(self.connection, id=id)
        if row:
            return NFT(**row)

        raise EntityDoesNotExist(f"nft with id {id} does not exist")

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

        async with self.connection.transaction():
            nft_in_db.updated_at = await queries.update_nft_by_id(
                self.connection,
                id=id,
                image_url=image_url,
            )

        return nft_in_db
