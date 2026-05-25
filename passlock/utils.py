"""Utility functions for passlock-cli"""

import os
import threading
import time
from pathlib import Path
from typing import Optional

import pyperclip


def get_passlock_dir() -> Path:
    """Return the passlock data directory path."""
    return Path.home() / ".passlock"


def get_salt_path() -> Path:
    """Return the salt file path."""
    return get_passlock_dir() / "salt.bin"


def get_verifier_path() -> Path:
    """Return the verifier file path."""
    return get_passlock_dir() / "verifier"


def get_vault_path() -> Path:
    """Return the vault file path."""
    return get_passlock_dir() / "vault.enc"


def ensure_passlock_dir() -> None:
    """Create passlock directory if it doesn't exist."""
    passlock_dir = get_passlock_dir()
    passlock_dir.mkdir(mode=0o700, exist_ok=True)


def atomic_write(path: Path, data: bytes) -> None:
    """
    Write data to file atomically with secure permissions.

    Uses a temporary file and atomic rename to prevent corruption.
    Sets file mode to 0o600 (owner read/write only).
    """
    temp_path = path.with_suffix(path.suffix + ".tmp")
    try:
        temp_path.write_bytes(data)
        os.chmod(temp_path, 0o600)
        temp_path.replace(path)
    except Exception:
        if temp_path.exists():
            temp_path.unlink()
        raise


def copy_to_clipboard_with_timer(text: str, timeout: int = 15) -> None:
    """
    Copy text to clipboard and clear it after timeout seconds.

    BLUE TEAM: Uses threading.Timer for reliable clearing.
    Overwrites with empty string then space to ensure clearing.
    Runs the clear operation in a background thread to avoid blocking.
    """
    pyperclip.copy(text)

    def clear_clipboard():
        # Check if clipboard still contains our text before clearing
        try:
            if pyperclip.paste() == text:
                # Overwrite with empty string
                pyperclip.copy("")
                # Then overwrite with space to ensure clearing
                time.sleep(0.1)
                pyperclip.copy(" ")
        except Exception:
            # Clipboard access may fail, ignore
            pass

    # Use Timer for more reliable scheduling
    timer = threading.Timer(timeout, clear_clipboard)
    timer.daemon = True
    timer.start()
