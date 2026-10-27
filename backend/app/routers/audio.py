import os
import urllib.parse
from pathlib import Path
from fastapi import APIRouter, Header, HTTPException, status, Request, Response, Query
from fastapi.responses import StreamingResponse
from backend.app.config import RAW_SOURCE_DIR

router = APIRouter(prefix="/api/audio", tags=["Audio"])

CHUNK_SIZE = 1024 * 512  # 512 KB

@router.head("/{filename}")
@router.get("/{filename}")
async def stream_audio(filename: str, request: Request, range: str = Header(None), download: int = Query(0)):
    """
    Stream audio file with HTTP 206 Partial Content support for seeking.
    Searches in RAW_SOURCE_DIR recursively.
    """
    from backend.app.config import DATA_DIR, BASE_DIR
    search_dirs = [RAW_SOURCE_DIR, DATA_DIR / "audio", DATA_DIR, BASE_DIR / "audio"]
    target_path = None
    for d in search_dirs:
        if d and d.exists():
            for p in d.rglob(filename):
                if p.is_file():
                    target_path = p
                    break
            if target_path:
                break
            
    if not target_path or not target_path.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Audio file '{filename}' not found.")

    file_size = target_path.stat().st_size

    resp_headers = {"Content-Length": str(file_size), "Accept-Ranges": "bytes"}
    if download:
        encoded_name = urllib.parse.quote(filename)
        resp_headers["Content-Disposition"] = f'attachment; filename="{encoded_name}"; filename*=UTF-8\'\'{encoded_name}'
        resp_headers["Access-Control-Expose-Headers"] = "Content-Disposition"

    if request.method == "HEAD":
        return Response(
            status_code=status.HTTP_200_OK,
            media_type="audio/mpeg",
            headers=resp_headers
        )
    
    if range is None:
        # Full content response
        def iter_full():
            with open(target_path, "rb") as f:
                while chunk := f.read(CHUNK_SIZE):
                    yield chunk
        return StreamingResponse(
            iter_full(),
            media_type="audio/mpeg",
            headers=resp_headers
        )

    # Parse Range header: bytes=start-end
    try:
        range_str = range.strip().lower()
        if not range_str.startswith("bytes="):
            raise ValueError("Invalid range prefix")
        byte_range = range_str[len("bytes="):]
        parts = byte_range.split("-")
        start = int(parts[0]) if parts[0] else 0
        end = int(parts[1]) if len(parts) > 1 and parts[1] else file_size - 1
        start = max(0, start)
        end = min(end, file_size - 1)
        if start > end:
            raise ValueError("Start greater than end")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
            headers={"Content-Range": f"bytes */{file_size}"}
        )

    content_length = end - start + 1

    def iter_chunk():
        with open(target_path, "rb") as f:
            f.seek(start)
            bytes_left = content_length
            while bytes_left > 0:
                read_size = min(CHUNK_SIZE, bytes_left)
                chunk = f.read(read_size)
                if not chunk:
                    break
                bytes_left -= len(chunk)
                yield chunk

    headers = {
        "Content-Range": f"bytes {start}-{end}/{file_size}",
        "Accept-Ranges": "bytes",
        "Content-Length": str(content_length),
    }
    if download:
        encoded_name = urllib.parse.quote(filename)
        headers["Content-Disposition"] = f'attachment; filename="{encoded_name}"; filename*=UTF-8\'\'{encoded_name}'
        headers["Access-Control-Expose-Headers"] = "Content-Disposition"

    return StreamingResponse(
        iter_chunk(),
        status_code=status.HTTP_206_PARTIAL_CONTENT,
        media_type="audio/mpeg",
        headers=headers
    )
