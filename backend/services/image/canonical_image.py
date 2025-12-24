from PIL import Image
import io

def normalize_to_canonical_jpeg(raw_bytes: bytes) -> bytes:
    img = Image.open(io.BytesIO(raw_bytes))
    img = img.convert("RGB")

    max_size = 2048
    img.thumbnail((max_size, max_size))

    out = io.BytesIO()
    img.save(out, format="JPEG", quality=85, optimize=True)
    return out.getvalue()
