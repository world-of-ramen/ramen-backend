from fastapi import APIRouter

from app.api.routes import authentication
from app.api.routes import comments
from app.api.routes import files
from app.api.routes import nfts
from app.api.routes import posts
from app.api.routes import stores
from app.api.routes import users

# from app.api.routes import profiles

router = APIRouter()
router.include_router(authentication.router, tags=["authentication"], prefix="/auth")
router.include_router(users.router, tags=["users"], prefix="/user")
router.include_router(nfts.router, tags=["nfts"], prefix="/nfts")
router.include_router(stores.router, tags=["stores"], prefix="/store")
router.include_router(files.router, tags=["files"], prefix="/file")
router.include_router(posts.router, tags=["posts"], prefix="/post")
router.include_router(comments.router, tags=["comments"], prefix="/comment")
