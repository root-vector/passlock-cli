"""Tests for crypto module"""

import pytest

from passlock.crypto import (
    create_verifier,
    decrypt_data,
    derive_key,
    encrypt_data,
    generate_salt,
    verify_password,
)


def test_generate_salt():
    """Test salt generation produces 16 bytes."""
    salt = generate_salt()
    assert len(salt) == 16
    assert isinstance(salt, bytes)


def test_generate_salt_unique():
    """Test that each salt is unique."""
    salt1 = generate_salt()
    salt2 = generate_salt()
    assert salt1 != salt2


def test_derive_key():
    """Test key derivation produces 32 bytes."""
    password = "test_password"
    salt = generate_salt()
    key = derive_key(password, salt)
    assert len(key) == 32
    assert isinstance(key, bytes)


def test_derive_key_deterministic():
    """Test that same password and salt produce same key."""
    password = "test_password"
    salt = generate_salt()
    key1 = derive_key(password, salt)
    key2 = derive_key(password, salt)
    assert key1 == key2


def test_derive_key_different_passwords():
    """Test that different passwords produce different keys."""
    salt = generate_salt()
    key1 = derive_key("password1", salt)
    key2 = derive_key("password2", salt)
    assert key1 != key2


def test_encrypt_decrypt_roundtrip():
    """Test encryption and decryption roundtrip."""
    password = "my_secure_password"
    salt = generate_salt()
    plaintext = b"This is a secret message"

    encrypted = encrypt_data(plaintext, password, salt)
    decrypted = decrypt_data(encrypted, password, salt)

    assert decrypted == plaintext
    assert encrypted != plaintext


def test_decrypt_wrong_password():
    """Test that decryption fails with wrong password."""
    password = "correct_password"
    wrong_password = "wrong_password"
    salt = generate_salt()
    plaintext = b"Secret data"

    encrypted = encrypt_data(plaintext, password, salt)

    with pytest.raises(Exception):
        decrypt_data(encrypted, wrong_password, salt)


def test_encrypt_unicode():
    """Test encryption of unicode data."""
    password = "password"
    salt = generate_salt()
    plaintext = "Hello 世界 🔒".encode("utf-8")

    encrypted = encrypt_data(plaintext, password, salt)
    decrypted = decrypt_data(encrypted, password, salt)

    assert decrypted == plaintext


def test_create_verifier():
    """Test verifier creation."""
    password = "test_password"
    verifier = create_verifier(password)
    assert isinstance(verifier, str)
    assert len(verifier) > 0


def test_verify_password_correct():
    """Test password verification with correct password."""
    password = "test_password"
    verifier = create_verifier(password)
    assert verify_password(password, verifier) is True


def test_verify_password_incorrect():
    """Test password verification with incorrect password."""
    password = "test_password"
    wrong_password = "wrong_password"
    verifier = create_verifier(password)
    assert verify_password(wrong_password, verifier) is False


def test_verifier_unique():
    """Test that verifiers are unique even for same password."""
    password = "test_password"
    verifier1 = create_verifier(password)
    verifier2 = create_verifier(password)
    # Verifiers should be different due to random salt in argon2
    assert verifier1 != verifier2
    # But both should verify the same password
    assert verify_password(password, verifier1) is True
    assert verify_password(password, verifier2) is True
