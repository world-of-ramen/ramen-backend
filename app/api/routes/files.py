from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import HTTPException
from fastapi import Query
from fastapi import UploadFile
from starlette.status import HTTP_400_BAD_REQUEST

from app.api.dependencies.authentication import get_current_user_authorizer
from app.api.dependencies.database import get_repository
from app.core.config import get_app_settings
from app.core.settings.app import AppSettings
from app.db.repositories.files import FilesRepository
from app.models.domain.users import User
from app.models.schemas.files import ObjectType
from app.models.schemas.files import UrlInResponse
from app.resources import strings

router = APIRouter()


@router.post("/upload", response_model=UrlInResponse, name="files:gcp-upload")
async def gcp_upload(
    file: UploadFile = File(..., description="A file read as UploadFile"),
    user: User = Depends(get_current_user_authorizer()),
    object_type: ObjectType = Query(ObjectType.user_post, description="ex: user_poost"),
    files_repo: FilesRepository = Depends(get_repository(FilesRepository)),
    settings: AppSettings = Depends(get_app_settings),
) -> UrlInResponse:
    try:
        public_url = files_repo.upload_image(
            user_id=user.id_,
            file=file,
            object_type=object_type,
            bucket_name=settings.bucket_name,
        )
    except TypeError:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=strings.UNABLE_TO_UPLOAD_IMAGE
        )

    return UrlInResponse(public_url=public_url)
