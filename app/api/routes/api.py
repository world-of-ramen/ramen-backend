from fastapi import APIRouter

from app.api.routes import authentication
from app.api.routes import files
from app.api.routes import stores
from app.api.routes import users

# from app.api.routes import profiles

router = APIRouter()
router.include_router(authentication.router, tags=["authentication"], prefix="/auth")
router.include_router(users.router, tags=["users"], prefix="/user")
# router.include_router(profiles.router, tags=["profiles"], prefix="/profiles")
router.include_router(stores.router, tags=["stores"], prefix="/store")
router.include_router(files.router, tags=["files"], prefix="/file")
