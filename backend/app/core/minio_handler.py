import random
import uuid
from datetime import datetime, timedelta
from fastapi import UploadFile, HTTPException, status
from minio import Minio, S3Error
from .config import settings


class MinioHandler():
    def __init__(self):
        self.client = Minio(
            endpoint=settings.minio.endpoint,
            access_key=settings.minio.access_key,
            secret_key=settings.minio.secret_key,
            secure=settings.minio.secure
        )


    async def create_buckets(self) -> None:
        buckets = [
            settings.minio.user_avatars_bucket,
            settings.minio.room_photos_bucket
        ]

        for bucket in buckets:
            if not self.client.bucket_exists(bucket):
                self.client.make_bucket(bucket)
                print(f"Bucket '{bucket}' created")
            else:
                print(f"Bucket '{bucket}' already exists")


    async def upload_user_photo(self, user_id: int, file: UploadFile) -> str:
        file_extension = file.filename.split('.')[-1]
        file_name = f"user_{user_id}.{file_extension}"

        try:
            self.client.put_object(
                bucket_name=settings.minio.user_avatars_bucket,
                object_name=file_name,
                data=file.file,
                length=file.size,
                content_type=file.content_type)
            return file_name
        except S3Error as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to upload file: {str(e)}")


    async def upload_room_photo(self, room_id: int, file: UploadFile) -> str:
        file_extension = file.filename.split('.')[-1]
        file_name = f"room_{room_id}_{uuid.uuid4()}.{file_extension}"

        try:
            self.client.put_object(
                bucket_name=settings.minio.room_photos_bucket,
                object_name=file_name,
                data=file.file,
                length=file.size,
                content_type=file.content_type
            )
            return file_name
        except S3Error as e:
            raise HTTPException(500, f"Failed to upload file: {str(e)}")


    async def get_public_url(self, bucket: str, file_name: str) -> str:
        return f"http://{settings.minio.endpoint}/{bucket}/{file_name}"


    async def delete_file(self, bucket: str, file_name: str):
        try:
            self.client.remove_object(bucket, file_name)
        except S3Error as e:
            raise HTTPException(500, f"Failed to delete file: {str(e)}")
