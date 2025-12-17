"""Upload API methods."""

from __future__ import annotations

import base64
import io
import os
from pathlib import Path
from typing import TYPE_CHECKING, BinaryIO

import httpx

from maxbot.errors import NetworkError, SerializationError
from maxbot.schemes import UploadEndpoint, UploadType, UploadedInfo

if TYPE_CHECKING:
    from maxbot.client import AsyncClient, Client


class Uploads:
    """File upload API."""

    def __init__(self, client: "Client") -> None:
        self._client = client

    def _get_upload_url(self, upload_type: UploadType) -> str:
        """Get upload URL for a specific type.

        Args:
            upload_type: Type of upload

        Returns:
            Upload URL
        """
        result = self._client.request_model(
            "POST",
            "uploads",
            UploadEndpoint,
            params={"type": upload_type.value},
            use_token_in_url=True,
        )
        return result.url

    def upload_media_from_file(
        self,
        filepath: str | Path,
        upload_type: UploadType = UploadType.FILE,
    ) -> UploadedInfo:
        """Upload media from a local file.

        Args:
            filepath: Path to the file
            upload_type: Type of upload

        Returns:
            Uploaded file info
        """
        filepath = Path(filepath)
        upload_url = self._get_upload_url(upload_type)

        with open(filepath, "rb") as f:
            return self._upload_from_reader(upload_url, f, filepath.name)

    def upload_media_from_reader(
        self,
        file: BinaryIO,
        filename: str,
        upload_type: UploadType = UploadType.FILE,
    ) -> UploadedInfo:
        """Upload media from a file-like object.

        Args:
            file: File-like object
            filename: Filename
            upload_type: Type of upload

        Returns:
            Uploaded file info
        """
        upload_url = self._get_upload_url(upload_type)
        return self._upload_from_reader(upload_url, file, filename)

    def upload_media_from_url(
        self,
        url: str,
        upload_type: UploadType = UploadType.FILE,
    ) -> UploadedInfo:
        """Upload media from a remote URL.

        Args:
            url: Remote file URL
            upload_type: Type of upload

        Returns:
            Uploaded file info
        """
        upload_url = self._get_upload_url(upload_type)

        # Download the file first
        try:
            response = httpx.get(url, timeout=60.0)
            response.raise_for_status()
        except httpx.RequestError as e:
            raise NetworkError("download", e)

        # Get filename from URL or Content-Disposition header
        filename = self._get_filename_from_response(response, url)

        return self._upload_from_reader(upload_url, io.BytesIO(response.content), filename)

    def upload_photo_from_file(self, filepath: str | Path) -> UploadedInfo:
        """Upload a photo from a local file.

        Args:
            filepath: Path to the photo file

        Returns:
            Uploaded photo info
        """
        return self.upload_media_from_file(filepath, UploadType.PHOTO)

    def upload_photo_from_reader(self, file: BinaryIO, filename: str) -> UploadedInfo:
        """Upload a photo from a file-like object.

        Args:
            file: File-like object
            filename: Filename

        Returns:
            Uploaded photo info
        """
        return self.upload_media_from_reader(file, filename, UploadType.PHOTO)

    def upload_photo_from_url(self, url: str) -> UploadedInfo:
        """Upload a photo from a remote URL.

        Args:
            url: Remote photo URL

        Returns:
            Uploaded photo info
        """
        return self.upload_media_from_url(url, UploadType.PHOTO)

    def upload_photo_from_base64(self, data: str, filename: str = "photo.jpg") -> UploadedInfo:
        """Upload a photo from base64 encoded string.

        Args:
            data: Base64 encoded image data
            filename: Filename

        Returns:
            Uploaded photo info
        """
        try:
            decoded = base64.b64decode(data)
        except Exception as e:
            raise SerializationError("decode", "base64", e)

        return self.upload_photo_from_reader(io.BytesIO(decoded), filename)

    def upload_video_from_file(self, filepath: str | Path) -> UploadedInfo:
        """Upload a video from a local file."""
        return self.upload_media_from_file(filepath, UploadType.VIDEO)

    def upload_audio_from_file(self, filepath: str | Path) -> UploadedInfo:
        """Upload audio from a local file."""
        return self.upload_media_from_file(filepath, UploadType.AUDIO)

    def _upload_from_reader(
        self,
        upload_url: str,
        file: BinaryIO,
        filename: str,
    ) -> UploadedInfo:
        """Upload file from reader to upload URL.

        Args:
            upload_url: Upload URL
            file: File-like object
            filename: Filename

        Returns:
            Uploaded file info
        """
        data = self._client.upload_file(upload_url, file, filename)
        return UploadedInfo.model_validate(data)

    @staticmethod
    def _get_filename_from_response(response: httpx.Response, url: str) -> str:
        """Get filename from response headers or URL.

        Args:
            response: HTTP response
            url: Original URL

        Returns:
            Filename
        """
        # Try Content-Disposition header
        content_disposition = response.headers.get("content-disposition", "")
        if "filename=" in content_disposition:
            parts = content_disposition.split("filename=")
            if len(parts) > 1:
                filename = parts[1].strip('"\'')
                return filename

        # Fall back to URL path
        return os.path.basename(url.split("?")[0]) or "file"


class AsyncUploads:
    """Async file upload API."""

    def __init__(self, client: "AsyncClient") -> None:
        self._client = client

    async def _get_upload_url(self, upload_type: UploadType) -> str:
        """Get upload URL for a specific type."""
        result = await self._client.request_model(
            "POST",
            "uploads",
            UploadEndpoint,
            params={"type": upload_type.value},
            use_token_in_url=True,
        )
        return result.url

    async def upload_media_from_file(
        self,
        filepath: str | Path,
        upload_type: UploadType = UploadType.FILE,
    ) -> UploadedInfo:
        """Upload media from a local file."""
        filepath = Path(filepath)
        upload_url = await self._get_upload_url(upload_type)

        with open(filepath, "rb") as f:
            return await self._upload_from_reader(upload_url, f, filepath.name)

    async def upload_media_from_reader(
        self,
        file: BinaryIO,
        filename: str,
        upload_type: UploadType = UploadType.FILE,
    ) -> UploadedInfo:
        """Upload media from a file-like object."""
        upload_url = await self._get_upload_url(upload_type)
        return await self._upload_from_reader(upload_url, file, filename)

    async def upload_media_from_url(
        self,
        url: str,
        upload_type: UploadType = UploadType.FILE,
    ) -> UploadedInfo:
        """Upload media from a remote URL."""
        upload_url = await self._get_upload_url(upload_type)

        async with httpx.AsyncClient() as http:
            try:
                response = await http.get(url, timeout=60.0)
                response.raise_for_status()
            except httpx.RequestError as e:
                raise NetworkError("download", e)

        filename = Uploads._get_filename_from_response(response, url)
        return await self._upload_from_reader(upload_url, io.BytesIO(response.content), filename)

    async def upload_photo_from_file(self, filepath: str | Path) -> UploadedInfo:
        """Upload a photo from a local file."""
        return await self.upload_media_from_file(filepath, UploadType.PHOTO)

    async def upload_photo_from_reader(self, file: BinaryIO, filename: str) -> UploadedInfo:
        """Upload a photo from a file-like object."""
        return await self.upload_media_from_reader(file, filename, UploadType.PHOTO)

    async def upload_photo_from_url(self, url: str) -> UploadedInfo:
        """Upload a photo from a remote URL."""
        return await self.upload_media_from_url(url, UploadType.PHOTO)

    async def upload_photo_from_base64(
        self, data: str, filename: str = "photo.jpg"
    ) -> UploadedInfo:
        """Upload a photo from base64 encoded string."""
        try:
            decoded = base64.b64decode(data)
        except Exception as e:
            raise SerializationError("decode", "base64", e)

        return await self.upload_photo_from_reader(io.BytesIO(decoded), filename)

    async def upload_video_from_file(self, filepath: str | Path) -> UploadedInfo:
        """Upload a video from a local file."""
        return await self.upload_media_from_file(filepath, UploadType.VIDEO)

    async def upload_audio_from_file(self, filepath: str | Path) -> UploadedInfo:
        """Upload audio from a local file."""
        return await self.upload_media_from_file(filepath, UploadType.AUDIO)

    async def _upload_from_reader(
        self,
        upload_url: str,
        file: BinaryIO,
        filename: str,
    ) -> UploadedInfo:
        """Upload file from reader to upload URL."""
        data = await self._client.upload_file(upload_url, file, filename)
        return UploadedInfo.model_validate(data)
