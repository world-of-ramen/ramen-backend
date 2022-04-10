import time

from fastapi import UploadFile
from google.cloud import storage

from app.db.errors import EntityDoesNotExist
from app.db.repositories.base import BaseRepository
from app.models.schemas.files import ObjectType


class FilesRepository(BaseRepository):
    def upload_image(
        self,
        *,
        user_id: int,
        file: UploadFile,
        object_type: ObjectType,
        bucket_name: str,
    ) -> str:
        file_ext = self._get_extension_from_mimetype(mimetype=file.content_type)
        epoch_time = str(int(time.time()))
        file_name = str(user_id) + "_" + epoch_time + "." + file_ext
        destination_blob_name = "images/" + object_type + "/" + file_name
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_file(file.file, content_type=file.content_type)

        return blob.public_url

    def _get_extension_from_mimetype(self, *, mimetype: str) -> str:
        if mimetype == "image/png":
            return "png"
        elif mimetype == "image/jpeg" or mimetype == "image/jpg":
            return "jpg"
        else:
            raise EntityDoesNotExist(f"Unsupported mime type: {mimetype}")
