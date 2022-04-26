from typing import List

from app.db.queries.queries import queries
from app.db.repositories.base import BaseRepository


class WhitelistContractsRepository(BaseRepository):
    async def get_whitelist_contract(self, *, id: int) -> List[str]:
        rows = await queries.get_whitelist_contracts(self.connection)
        list = []
        for row in rows:
            list.append[row]
