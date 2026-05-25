"""Vault operations for passlock-cli"""

import json
import logging
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from cryptography.fernet import InvalidToken

from .crypto import decrypt_data, encrypt_data
from .utils import atomic_write, get_salt_path, get_vault_path

logger = logging.getLogger(__name__)


class VaultEntry:
    """Represents a single password entry in the vault."""

    def __init__(
        self,
        site: str,
        username: str,
        password: str,
        notes: str = "",
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
    ):
        # BLUE TEAM: Input validation - sanitize inputs
        self.site = self._sanitize_input(site, max_length=256)
        self.username = self._sanitize_input(username, max_length=256)
        self.password = password  # Don't sanitize password
        self.notes = self._sanitize_input(notes, max_length=1024)
        self.created_at = created_at or datetime.now(timezone.utc).isoformat()
        self.updated_at = updated_at or datetime.now(timezone.utc).isoformat()

    @staticmethod
    def _sanitize_input(text: str, max_length: int) -> str:
        """Sanitize input by removing control characters and limiting length."""
        # Remove control characters except newline and tab
        sanitized = re.sub(r"[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f]", "", text)
        # Limit length
        return sanitized[:max_length]

    def to_dict(self) -> Dict:
        """Convert entry to dictionary for JSON serialization."""
        return {
            "site": self.site,
            "username": self.username,
            "password": self.password,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "VaultEntry":
        """Create entry from dictionary."""
        return cls(**data)


class Vault:
    """Manages the encrypted password vault."""

    def __init__(self, entries: Optional[List[VaultEntry]] = None):
        self.entries = entries or []
        self.version = 1

    def to_dict(self) -> Dict:
        """Convert vault to dictionary for JSON serialization."""
        return {
            "version": self.version,
            "entries": [entry.to_dict() for entry in self.entries],
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Vault":
        """Create vault from dictionary."""
        entries = [VaultEntry.from_dict(e) for e in data.get("entries", [])]
        vault = cls(entries)
        vault.version = data.get("version", 1)
        return vault

    def add_entry(self, entry: VaultEntry) -> None:
        """Add or update an entry. Updates if site already exists."""
        existing = self.find_entry(entry.site)
        if existing:
            existing.username = entry.username
            existing.password = entry.password
            existing.notes = entry.notes
            existing.updated_at = datetime.now(timezone.utc).isoformat()
            logger.info(f"Updated entry for site: {entry.site}")
        else:
            self.entries.append(entry)
            logger.info(f"Added entry for site: {entry.site}")

    def find_entry(self, site: str) -> Optional[VaultEntry]:
        """Find entry by site name (case-insensitive)."""
        site_lower = site.lower()
        for entry in self.entries:
            if entry.site.lower() == site_lower:
                return entry
        return None

    def delete_entry(self, site: str) -> bool:
        """Delete entry by site name. Returns True if deleted, False if not found."""
        entry = self.find_entry(site)
        if entry:
            self.entries.remove(entry)
            logger.info(f"Deleted entry for site: {site}")
            return True
        return False

    def list_entries(self) -> List[VaultEntry]:
        """Return all entries sorted by site name."""
        return sorted(self.entries, key=lambda e: e.site.lower())


def load_vault(master_password: str) -> Vault:
    """
    Load and decrypt the vault from disk.

    Raises FileNotFoundError if vault doesn't exist.
    Raises InvalidToken if password is wrong.
    Raises PermissionError if file permissions are insecure.
    """
    vault_path = get_vault_path()
    salt_path = get_salt_path()

    if not vault_path.exists():
        raise FileNotFoundError("Vault not found. Run 'passlock init' first.")

    # BLUE TEAM: Check file permissions before loading
    _check_file_permissions(vault_path)
    _check_file_permissions(salt_path)

    salt = salt_path.read_bytes()
    encrypted_data = vault_path.read_bytes()

    try:
        decrypted_data = decrypt_data(encrypted_data, master_password, salt)
        vault_dict = json.loads(decrypted_data.decode("utf-8"))
        return Vault.from_dict(vault_dict)
    except InvalidToken:
        raise ValueError("Invalid master password")
    except json.JSONDecodeError:
        raise ValueError("Vault is corrupted")


def _check_file_permissions(file_path: Path) -> None:
    """
    BLUE TEAM: Verify file has secure permissions (0o600).

    Raises PermissionError if permissions are too permissive.
    """
    import platform

    # Only check on Unix-like systems (not Windows)
    if platform.system() == "Windows":
        return

    stat_info = file_path.stat()
    mode = stat_info.st_mode & 0o777

    if mode != 0o600:
        raise PermissionError(
            f"Insecure file permissions on {file_path.name}: {oct(mode)}. "
            f"Fix with: chmod 0o600 {file_path}"
        )


def save_vault(vault: Vault, master_password: str) -> None:
    """
    Encrypt and save the vault to disk atomically.

    Uses atomic write to prevent corruption if interrupted.
    """
    vault_path = get_vault_path()
    salt_path = get_salt_path()

    salt = salt_path.read_bytes()
    vault_json = json.dumps(vault.to_dict(), indent=2)
    encrypted_data = encrypt_data(vault_json.encode("utf-8"), master_password, salt)

    atomic_write(vault_path, encrypted_data)
    logger.info("Vault saved successfully")


def create_empty_vault(master_password: str, salt: bytes) -> None:
    """Create a new empty encrypted vault."""
    vault = Vault()
    vault_json = json.dumps(vault.to_dict(), indent=2)
    encrypted_data = encrypt_data(vault_json.encode("utf-8"), master_password, salt)

    vault_path = get_vault_path()
    atomic_write(vault_path, encrypted_data)
    logger.info("Empty vault created")
