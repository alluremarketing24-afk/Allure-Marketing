# core/utils/supabase_upload.py
from supabase import create_client
from PIL import Image
import io, os, posixpath

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def _read_file_bytes(file_obj) -> bytes:
    try:
        if hasattr(file_obj, "seek"):
            file_obj.seek(0)
    except Exception:
        pass

    if hasattr(file_obj, "chunks"):
        return b"".join(chunk for chunk in file_obj.chunks())
    return file_obj.read()


def _convert_to_webp(file_bytes, orig_name: str) -> tuple[bytes, str]:
    """Convert image bytes to WebP and return (webp_bytes, new_name)."""
    try:
        img = Image.open(io.BytesIO(file_bytes)).convert("RGB")
        output = io.BytesIO()
        img.save(output, format="WEBP", quality=80)
        output.seek(0)

        # Replace extension with .webp
        if "." in orig_name:
            stem = orig_name.rsplit(".", 1)[0]
        else:
            stem = orig_name
        return output.read(), f"{stem}.webp"
    except Exception:
        # If not an image, return original
        return file_bytes, orig_name


def _file_exists(bucket_name: str, path: str) -> bool:
    directory = posixpath.dirname(path) or ""
    filename = posixpath.basename(path)
    items = supabase.storage.from_(bucket_name).list(path=directory)
    return any(item.get("name") == filename for item in items)


def _unique_path(bucket_name: str, desired_path: str) -> str:
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
    file_bytes = _read_file_bytes(file_obj)

    # 🔥 Try to auto-convert to WebP
    file_bytes, target_path = _convert_to_webp(file_bytes, target_path)

    final_path = target_path
    if not overwrite and rename_on_conflict:
        final_path = _unique_path(bucket_name, target_path)

    file_options = {"upsert": bool(overwrite)}
    response = supabase.storage.from_(bucket_name).upload(
        path=final_path,
        file=file_bytes,
        file_options=file_options,
    )

    error = getattr(response, "error", None) if hasattr(response, "error") else (response.get("error") if isinstance(response, dict) else None)
    if error:
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
