"""Cryptographic operations for passlock-cli"""

import base64
import os
import secrets
from typing import Tuple

from argon2 import PasswordHasher
from argon2.low_level import Type, hash_secret_raw
from cryptography.fernet import Fernet, InvalidToken

# Argon2id parameters for key derivation
TIME_COST = 3
MEMORY_COST = 65536  # 64 MiB
PARALLELISM = 4
HASH_LEN = 32  # 32 bytes for Fernet key


def generate_salt() -> bytes:
    """Generate a cryptographically secure random 16-byte salt."""
    return os.urandom(16)


def derive_key(password: str, salt: bytes) -> bytes:
    """
    Derive a 32-byte encryption key from password using Argon2id.

    Uses Argon2id with time_cost=3, memory_cost=64MiB, parallelism=4.
    This provides strong protection against brute-force attacks while
    remaining fast enough for interactive use (~100-300ms on modern hardware).

    Returns raw 32-byte key suitable for Fernet (after base64 encoding).
    """
    return hash_secret_raw(
        secret=password.encode("utf-8"),
        salt=salt,
        time_cost=TIME_COST,
        memory_cost=MEMORY_COST,
        parallelism=PARALLELISM,
        hash_len=HASH_LEN,
        type=Type.ID,
    )


def key_to_fernet(key: bytes) -> Fernet:
    """Convert raw 32-byte key to Fernet cipher instance."""
    fernet_key = base64.urlsafe_b64encode(key)
    return Fernet(fernet_key)


def encrypt_data(data: bytes, password: str, salt: bytes) -> bytes:
    """Encrypt data using password-derived key."""
    key = derive_key(password, salt)
    try:
        fernet = key_to_fernet(key)
        encrypted = fernet.encrypt(data)
        return encrypted
    finally:
        # BLUE TEAM: Wipe key from memory
        del key


def decrypt_data(encrypted_data: bytes, password: str, salt: bytes) -> bytes:
    """
    Decrypt data using password-derived key.

    Raises InvalidToken if password is wrong or data is corrupted.
    """
    key = derive_key(password, salt)
    try:
        fernet = key_to_fernet(key)
        decrypted = fernet.decrypt(encrypted_data)
        return decrypted
    finally:
        # BLUE TEAM: Wipe key from memory
        del key


def create_verifier(password: str) -> str:
    """
    Create an Argon2id hash of the master password for verification.

    This hash is stored on disk and used to verify the master password
    without storing the password itself. Uses argon2-cffi's PasswordHasher
    with secure defaults.
    """
    ph = PasswordHasher()
    return ph.hash(password)


def verify_password(password: str, verifier_hash: str) -> bool:
    """
    Verify password against stored verifier hash using constant-time comparison.

    BLUE TEAM: Uses argon2's built-in constant-time verification.
    Returns True if password matches, False otherwise.
    Does not raise exceptions on mismatch.
    """
    ph = PasswordHasher(
        time_cost=TIME_COST,
        memory_cost=MEMORY_COST,
        parallelism=PARALLELISM,
        hash_len=HASH_LEN,
        type=Type.ID,
    )
    try:
        ph.verify(verifier_hash, password)
        return True
    except Exception:
        return False
