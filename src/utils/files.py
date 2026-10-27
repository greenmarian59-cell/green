import uuid, aiofiles
from pathlib import Path
from fastapi import UploadFile, HTTPException

MEDIA_DIR = Path("media")

MEDIA_FORMAT = {
    "image/jpeg": ".jpeg",
    "image/png": ".png",
    "image/webp": ".webp",
}

async def save_image(file: UploadFile) -> str:
    media_bb = MEDIA_FORMAT.get(file.content_type)
    if not media_bb:
        raise HTTPException(400, "Only jpg,png,webp format is supported")
    MEDIA_DIR.mkdir(parents=True, exist_ok=True)
    path = MEDIA_DIR / f"{uuid.uuid4().hex}{media_bb}"
    async with aiofiles.open(path, "wb") as f:
        while chunk := await file.read(1024*1024):
            await f.write(chunk)
            return path.as_posix()


def delete_file(path:str | None):
    if path:
        Path(path).unlink(missing_ok=True)

