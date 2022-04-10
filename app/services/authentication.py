from app.db.errors import EntityDoesNotExist
from app.db.repositories.users import UsersRepository


async def check_wallet_address_is_taken(
    repo: UsersRepository, wallet_address: str
) -> bool:
    try:
        await repo.get_user_by_wallet_address(wallet_address=wallet_address)
    except EntityDoesNotExist:
        return False

    return True
