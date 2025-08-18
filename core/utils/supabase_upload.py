# core/utils/supabase_upload.py
from supabase import create_client
import os
import posixpath

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def _read_file_bytes(file_obj) -> bytes:
    """Read bytes from Django UploadedFile or file-like safely."""
    try:
        if hasattr(file_obj, "seek"):
            file_obj.seek(0)
    except Exception:
        pass

    if hasattr(file_obj, "chunks"):
        return b"".join(chunk for chunk in file_obj.chunks())
    return file_obj.read()


def _file_exists(bucket_name: str, path: str) -> bool:
    """Check if a file already exists at path inside the bucket."""
    directory = posixpath.dirname(path) or ""
    filename = posixpath.basename(path)
    items = supabase.storage.from_(bucket_name).list(path=directory)
    return any(item.get("name") == filename for item in items)


def _unique_path(bucket_name: str, desired_path: str) -> str:
    """Return a conflict-free path by appending -1, -2, ... before the extension."""
    if not _file_exists(bucket_name, desired_path):
        return desired_path

    directory = posixpath.dirname(desired_path) or ""
    filename = posixpath.basename(desired_path)

    if "." in filename:
        stem, ext = filename.rsplit(".", 1)
        ext = "." + ext
    else:
        stem, ext = filename, ""

    i = 1
    while True:
        candidate = f"{stem}-{i}{ext}"
        candidate_path = posixpath.join(directory, candidate) if directory else candidate
        if not _file_exists(bucket_name, candidate_path):
            return candidate_path
        i += 1


def upload_to_supabase(bucket_name, file_obj, target_path, *, rename_on_conflict=True, overwrite=False):
    """
    Upload to Supabase Storage and return the public URL (string).
    - rename_on_conflict=True: auto-renames to name-1.ext, name-2.ext, ...
    - overwrite=True: upsert to the same path (no auto-rename)
    """
    file_bytes = _read_file_bytes(file_obj)

    final_path = target_path
    if not overwrite and rename_on_conflict:
        final_path = _unique_path(bucket_name, target_path)

    # Python client supports file_options={"upsert": True} for overwrites
    file_options = {"upsert": bool(overwrite)}

    response = supabase.storage.from_(bucket_name).upload(
        path=final_path,
        file=file_bytes,
        file_options=file_options,
    )

    # Handle both dict and object styles
    error = getattr(response, "error", None) if hasattr(response, "error") else (response.get("error") if isinstance(response, dict) else None)
    if error:
        # Last-resort rename if server still complained about conflict
        if not overwrite and rename_on_conflict:
            final_path = _unique_path(bucket_name, target_path)
            response = supabase.storage.from_(bucket_name).upload(
                path=final_path,
                file=file_bytes,
                file_options={"upsert": False},
            )
            error = getattr(response, "error", None) if hasattr(response, "error") else (response.get("error") if isinstance(response, dict) else None)
            if error:
                raise Exception("Supabase upload failed", error)
        else:
            raise Exception("Supabase upload failed", error)

    return supabase.storage.from_(bucket_name).get_public_url(final_path)
