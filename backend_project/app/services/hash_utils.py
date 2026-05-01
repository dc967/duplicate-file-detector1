import hashlib
import os

# Chunk size — bade files ke liye
CHUNK_SIZE = 65536  # 64 KB



def get_file_hash(filepath: str, algorithm: str = "sha256") -> str | None:
    """File ka hash calculate karo"""
    try:
        # Algorithm select karo
        if algorithm == "md5":
            hasher = hashlib.md5()
        elif algorithm == "sha512":
            hasher = hashlib.sha512()
        else:
            hasher = hashlib.sha256()

        # File chunks mein padho
        with open(filepath, "rb") as f:
            while chunk := f.read(CHUNK_SIZE):
                hasher.update(chunk)

        return hasher.hexdigest()

    except (OSError, PermissionError):
        return None



def get_quick_hash(filepath: str) -> str | None:
    """
    Sirf pehle aur aakhri 64KB padhta hai
    Large files ke liye fast pre-filter
    """
    try:
        hasher = hashlib.sha256()
        file_size = os.path.getsize(filepath)

        with open(filepath, "rb") as f:
            # Pehle 64KB
            hasher.update(f.read(CHUNK_SIZE))

            # Aakhri 64KB — sirf bade files ke liye
            if file_size > CHUNK_SIZE * 2:
                f.seek(-CHUNK_SIZE, 2)
                hasher.update(f.read(CHUNK_SIZE))

        # File size bhi hash mein add karo
        hasher.update(str(file_size).encode())

        return hasher.hexdigest()

    except (OSError, PermissionError):
        return None



def get_file_type(extension: str) -> str:
    """Extension se file type pata karo"""
    extension = extension.lower()

    image_types = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp', 'svg']
    video_types = ['mp4', 'avi', 'mov', 'mkv', 'wmv', 'flv']
    audio_types = ['mp3', 'wav', 'flac', 'aac', 'm4a']
    doc_types   = ['pdf', 'docx', 'doc', 'txt', 'xlsx', 'pptx']
    archive_types = ['zip', 'rar', '7z', 'tar', 'gz']

    if extension in image_types:
        return "image"
    elif extension in video_types:
        return "video"
    elif extension in audio_types:
        return "audio"
    elif extension in doc_types:
        return "document"
    elif extension in archive_types:
        return "archive"
    else:
        return "other"



def format_file_size(size_bytes: int) -> str:
    """Bytes ko readable format mein convert karo"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"