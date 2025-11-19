"""
Utility functions for the nflverse data fetcher
"""

import os
import hashlib
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional


def ensure_cache_dir(cache_dir: str) -> Path:
    """
    Ensure the cache directory exists.

    Args:
        cache_dir: Path to the cache directory

    Returns:
        Path object for the cache directory
    """
    cache_path = Path(cache_dir)
    cache_path.mkdir(parents=True, exist_ok=True)
    return cache_path


def get_cache_key(url: str) -> str:
    """
    Generate a cache key for a given URL.

    Args:
        url: The URL to generate a key for

    Returns:
        A hash string to use as cache key
    """
    return hashlib.md5(url.encode()).hexdigest()


def is_cache_valid(cache_file: Path, expiry_days: int) -> bool:
    """
    Check if a cached file is still valid.

    Args:
        cache_file: Path to the cached file
        expiry_days: Number of days before cache expires

    Returns:
        True if cache is valid, False otherwise
    """
    if not cache_file.exists():
        return False

    mtime = datetime.fromtimestamp(cache_file.stat().st_mtime)
    expiry = datetime.now() - timedelta(days=expiry_days)

    return mtime > expiry


def save_cache_metadata(cache_dir: Path, url: str, filename: str, metadata: dict):
    """
    Save metadata about a cached file.

    Args:
        cache_dir: Cache directory path
        url: Original URL
        filename: Cached filename
        metadata: Metadata dictionary to save
    """
    meta_file = cache_dir / f"{get_cache_key(url)}.meta"

    meta_data = {
        "url": url,
        "filename": filename,
        "cached_at": datetime.now().isoformat(),
        **metadata
    }

    with open(meta_file, 'w') as f:
        json.dump(meta_data, f, indent=2)


def load_cache_metadata(cache_dir: Path, url: str) -> Optional[dict]:
    """
    Load metadata about a cached file.

    Args:
        cache_dir: Cache directory path
        url: Original URL

    Returns:
        Metadata dictionary or None if not found
    """
    meta_file = cache_dir / f"{get_cache_key(url)}.meta"

    if not meta_file.exists():
        return None

    try:
        with open(meta_file, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None
