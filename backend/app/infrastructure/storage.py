"""
IndusMind AI — File Storage Infrastructure

Local file storage with S3-compatible interface for future migration.
"""

from __future__ import annotations

from pathlib import Path

import aiofiles

from app.core.config import get_settings
from app.core.exceptions import StorageError
from app.core.logging import get_logger

settings = get_settings()
logger = get_logger(__name__)


class FileStorage:
    """Local file storage with organized directory structure."""

    def __init__(self) -> None:
        self.base_path = Path(settings.UPLOAD_DIR)
        self._ensure_directories()

    def _ensure_directories(self) -> None:
        """Create required storage directories."""
        for subdir in ["originals", "extracted", "thumbnails"]:
            (self.base_path / subdir).mkdir(parents=True, exist_ok=True)

    async def save_file(
        self,
        file_content: bytes,
        original_filename: str,
        document_id: str,
    ) -> str:
        """Save an uploaded file. Returns the storage path."""
        ext = Path(original_filename).suffix.lower()
        filename = f"{document_id}{ext}"
        file_path = self.base_path / "originals" / filename

        try:
            async with aiofiles.open(file_path, "wb") as f:
                await f.write(file_content)
            logger.info("File saved", path=str(file_path), size=len(file_content))
            return str(file_path)
        except Exception as err:
            raise StorageError(f"Failed to save file: {err}") from err

    async def save_extracted_text(self, document_id: str, text: str) -> str:
        """Save extracted text from a document."""
        file_path = self.base_path / "extracted" / f"{document_id}.txt"
        try:
            async with aiofiles.open(file_path, "w", encoding="utf-8") as f:
                await f.write(text)
            return str(file_path)
        except Exception as err:
            raise StorageError(f"Failed to save extracted text: {err}") from err

    async def read_file(self, file_path: str) -> bytes:
        """Read a file from storage."""
        try:
            async with aiofiles.open(file_path, "rb") as f:
                return await f.read()
        except FileNotFoundError as err:
            raise StorageError(f"File not found: {file_path}") from err

    async def delete_file(self, file_path: str) -> None:
        """Delete a file from storage."""
        try:
            path = Path(file_path)
            if path.exists():
                path.unlink()
                logger.info("File deleted", path=file_path)
        except Exception as e:
            logger.warning("Failed to delete file", path=file_path, error=str(e))

    async def delete_document_files(self, document_id: str) -> None:
        """Delete all files associated with a document."""
        for subdir in ["originals", "extracted", "thumbnails"]:
            dir_path = self.base_path / subdir
            for file in dir_path.glob(f"{document_id}*"):
                file.unlink(missing_ok=True)

    def get_storage_stats(self) -> dict:
        """Get storage usage statistics."""
        total_size = 0
        file_count = 0
        for file in self.base_path.rglob("*"):
            if file.is_file():
                total_size += file.stat().st_size
                file_count += 1
        return {
            "total_files": file_count,
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
        }


# Singleton
file_storage = FileStorage()
