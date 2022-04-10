from fastapi import APIRouter

from app.api.routes import stores

# from app.api.routes import authentication
# from app.api.routes import profiles
# from app.api.routes import users

router = APIRouter()
# router.include_router(authentication.router, tags=["authentication"], prefix="/users")
# router.include_router(users.router, tags=["users"], prefix="/user")
# router.include_router(profiles.router, tags=["profiles"], prefix="/profiles")
router.include_router(stores.router, tags=["stores"], prefix="/store")
