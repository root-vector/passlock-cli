"""Tests for vault module"""

import json
import tempfile
from pathlib import Path

import pytest

from passlock.crypto import generate_salt
from passlock.vault import Vault, VaultEntry, create_empty_vault, load_vault, save_vault


def test_vault_entry_creation():
    """Test creating a vault entry."""
    entry = VaultEntry(
        site="example.com", username="user@example.com", password="secret123", notes="Test note"
    )
    assert entry.site == "example.com"
    assert entry.username == "user@example.com"
    assert entry.password == "secret123"
    assert entry.notes == "Test note"
    assert entry.created_at is not None
    assert entry.updated_at is not None


def test_vault_entry_to_dict():
    """Test converting entry to dictionary."""
    entry = VaultEntry(site="test.com", username="user", password="pass")
    data = entry.to_dict()
    assert data["site"] == "test.com"
    assert data["username"] == "user"
    assert data["password"] == "pass"
    assert "created_at" in data
    assert "updated_at" in data


def test_vault_entry_from_dict():
    """Test creating entry from dictionary."""
    data = {
        "site": "test.com",
        "username": "user",
        "password": "pass",
        "notes": "note",
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00",
    }
    entry = VaultEntry.from_dict(data)
    assert entry.site == "test.com"
    assert entry.username == "user"
    assert entry.password == "pass"
    assert entry.notes == "note"


def test_vault_add_entry():
    """Test adding entry to vault."""
    vault = Vault()
    entry = VaultEntry(site="test.com", username="user", password="pass")
    vault.add_entry(entry)
    assert len(vault.entries) == 1
    assert vault.entries[0].site == "test.com"


def test_vault_add_duplicate_updates():
    """Test adding duplicate entry updates existing."""
    vault = Vault()
    entry1 = VaultEntry(site="test.com", username="user1", password="pass1")
    entry2 = VaultEntry(site="test.com", username="user2", password="pass2")

    vault.add_entry(entry1)
    assert len(vault.entries) == 1

    vault.add_entry(entry2)
    assert len(vault.entries) == 1
    assert vault.entries[0].username == "user2"
    assert vault.entries[0].password == "pass2"


def test_vault_find_entry():
    """Test finding entry by site."""
    vault = Vault()
    entry = VaultEntry(site="test.com", username="user", password="pass")
    vault.add_entry(entry)

    found = vault.find_entry("test.com")
    assert found is not None
    assert found.site == "test.com"


def test_vault_find_entry_case_insensitive():
    """Test finding entry is case-insensitive."""
    vault = Vault()
    entry = VaultEntry(site="Test.Com", username="user", password="pass")
    vault.add_entry(entry)

    found = vault.find_entry("test.com")
    assert found is not None
    assert found.site == "Test.Com"


def test_vault_find_entry_not_found():
    """Test finding non-existent entry returns None."""
    vault = Vault()
    found = vault.find_entry("nonexistent.com")
    assert found is None


def test_vault_delete_entry():
    """Test deleting entry from vault."""
    vault = Vault()
    entry = VaultEntry(site="test.com", username="user", password="pass")
    vault.add_entry(entry)

    result = vault.delete_entry("test.com")
    assert result is True
    assert len(vault.entries) == 0


def test_vault_delete_nonexistent():
    """Test deleting non-existent entry returns False."""
    vault = Vault()
    result = vault.delete_entry("nonexistent.com")
    assert result is False


def test_vault_list_entries():
    """Test listing entries sorted by site."""
    vault = Vault()
    vault.add_entry(VaultEntry(site="zebra.com", username="user", password="pass"))
    vault.add_entry(VaultEntry(site="apple.com", username="user", password="pass"))
    vault.add_entry(VaultEntry(site="middle.com", username="user", password="pass"))

    entries = vault.list_entries()
    assert len(entries) == 3
    assert entries[0].site == "apple.com"
    assert entries[1].site == "middle.com"
    assert entries[2].site == "zebra.com"


def test_vault_to_dict():
    """Test converting vault to dictionary."""
    vault = Vault()
    vault.add_entry(VaultEntry(site="test.com", username="user", password="pass"))

    data = vault.to_dict()
    assert data["version"] == 1
    assert len(data["entries"]) == 1
    assert data["entries"][0]["site"] == "test.com"


def test_vault_from_dict():
    """Test creating vault from dictionary."""
    data = {
        "version": 1,
        "entries": [
            {
                "site": "test.com",
                "username": "user",
                "password": "pass",
                "notes": "",
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00",
            }
        ],
    }
    vault = Vault.from_dict(data)
    assert vault.version == 1
    assert len(vault.entries) == 1
    assert vault.entries[0].site == "test.com"


def test_create_and_load_vault(tmp_path, monkeypatch):
    """Test creating and loading encrypted vault."""
    import os

    # Mock paths to use temp directory
    salt_path = tmp_path / "salt.bin"
    vault_path = tmp_path / "vault.enc"

    monkeypatch.setattr("passlock.vault.get_salt_path", lambda: salt_path)
    monkeypatch.setattr("passlock.vault.get_vault_path", lambda: vault_path)

    password = "test_password"
    salt = generate_salt()
    salt_path.write_bytes(salt)
    os.chmod(salt_path, 0o600)  # Set secure permissions

    # Create empty vault
    create_empty_vault(password, salt)
    assert vault_path.exists()

    # Load vault
    vault = load_vault(password)
    assert len(vault.entries) == 0
    assert vault.version == 1


def test_save_and_load_vault_with_entries(tmp_path, monkeypatch):
    """Test saving and loading vault with entries."""
    import os

    salt_path = tmp_path / "salt.bin"
    vault_path = tmp_path / "vault.enc"

    monkeypatch.setattr("passlock.vault.get_salt_path", lambda: salt_path)
    monkeypatch.setattr("passlock.vault.get_vault_path", lambda: vault_path)

    password = "test_password"
    salt = generate_salt()
    salt_path.write_bytes(salt)
    os.chmod(salt_path, 0o600)  # Set secure permissions

    # Create vault with entries
    vault = Vault()
    vault.add_entry(VaultEntry(site="test.com", username="user", password="pass123"))
    vault.add_entry(VaultEntry(site="example.com", username="admin", password="secret"))

    save_vault(vault, password)

    # Load and verify
    loaded_vault = load_vault(password)
    assert len(loaded_vault.entries) == 2

    entry1 = loaded_vault.find_entry("test.com")
    assert entry1 is not None
    assert entry1.username == "user"
    assert entry1.password == "pass123"

    entry2 = loaded_vault.find_entry("example.com")
    assert entry2 is not None
    assert entry2.username == "admin"
    assert entry2.password == "secret"


def test_load_vault_wrong_password(tmp_path, monkeypatch):
    """Test loading vault with wrong password fails."""
    import os

    salt_path = tmp_path / "salt.bin"
    vault_path = tmp_path / "vault.enc"

    monkeypatch.setattr("passlock.vault.get_salt_path", lambda: salt_path)
    monkeypatch.setattr("passlock.vault.get_vault_path", lambda: vault_path)

    password = "correct_password"
    wrong_password = "wrong_password"
    salt = generate_salt()
    salt_path.write_bytes(salt)
    os.chmod(salt_path, 0o600)  # Set secure permissions

    create_empty_vault(password, salt)

    with pytest.raises(ValueError, match="Invalid master password"):
        load_vault(wrong_password)


def test_load_vault_not_found(tmp_path, monkeypatch):
    """Test loading non-existent vault raises error."""
    vault_path = tmp_path / "vault.enc"
    monkeypatch.setattr("passlock.vault.get_vault_path", lambda: vault_path)

    with pytest.raises(FileNotFoundError):
        load_vault("password")
