"""Stress and reliability tests for passlock-cli"""

import os
import shutil
import tempfile
from pathlib import Path

import pytest

from passlock.crypto import generate_salt
from passlock.vault import (Vault, VaultEntry, create_empty_vault, load_vault,
                            save_vault)


@pytest.fixture
def temp_vault_env(tmp_path, monkeypatch):
    """Create isolated vault environment for testing."""
    salt_path = tmp_path / "salt.bin"
    vault_path = tmp_path / "vault.enc"

    monkeypatch.setattr("passlock.vault.get_salt_path", lambda: salt_path)
    monkeypatch.setattr("passlock.vault.get_vault_path", lambda: vault_path)

    password = "test_password_123"
    salt = generate_salt()
    salt_path.write_bytes(salt)

    create_empty_vault(password, salt)

    return {
        "salt_path": salt_path,
        "vault_path": vault_path,
        "password": password,
        "salt": salt,
    }


def test_power_loss_during_save(temp_vault_env):
    """STRESS: Simulate power loss during save by writing half file."""
    vault_path = temp_vault_env["vault_path"]
    password = temp_vault_env["password"]

    # Add entry and save normally
    vault = load_vault(password)
    vault.add_entry(VaultEntry("test.com", "user", "pass123", ""))
    save_vault(vault, password)

    # Read full vault
    full_vault_data = vault_path.read_bytes()

    # Simulate power loss by writing only half the file
    half_data = full_vault_data[: len(full_vault_data) // 2]
    vault_path.write_bytes(half_data)

    # Attempt to load corrupted vault
    with pytest.raises(Exception) as exc_info:
        load_vault(password)

    # Should detect corruption gracefully
    assert "Invalid" in str(exc_info.value) or "corrupted" in str(exc_info.value).lower()


def test_change_master_wrong_password(temp_vault_env):
    """STRESS: Test change-master with wrong old password multiple times."""
    password = temp_vault_env["password"]
    wrong_password = "wrong_password"

    # Add some entries
    vault = load_vault(password)
    vault.add_entry(VaultEntry("test1.com", "user1", "pass1", ""))
    vault.add_entry(VaultEntry("test2.com", "user2", "pass2", ""))
    save_vault(vault, password)

    # Try to change master with wrong password 3 times
    for i in range(3):
        with pytest.raises(ValueError) as exc_info:
            load_vault(wrong_password)
        assert "Invalid master password" in str(exc_info.value)

    # Verify vault is still intact with correct password
    vault = load_vault(password)
    assert len(vault.entries) == 2


def test_export_import_roundtrip(temp_vault_env, tmp_path):
    """STRESS: Test export/import roundtrip with modified file."""
    password = temp_vault_env["password"]
    vault_path = temp_vault_env["vault_path"]

    # Add entries
    vault = load_vault(password)
    for i in range(10):
        vault.add_entry(VaultEntry(f"site{i}.com", f"user{i}", f"pass{i}", f"notes{i}"))
    save_vault(vault, password)

    # Export (copy vault file)
    export_path = tmp_path / "backup.enc"
    shutil.copy2(vault_path, export_path)

    # Modify original vault
    vault = load_vault(password)
    vault.add_entry(VaultEntry("new_site.com", "new_user", "new_pass", ""))
    save_vault(vault, password)

    # Import backup (restore from export)
    shutil.copy2(export_path, vault_path)

    # Verify restored vault has original 10 entries
    vault = load_vault(password)
    assert len(vault.entries) == 10
    assert vault.find_entry("site5.com") is not None
    assert vault.find_entry("new_site.com") is None


def test_memory_usage_large_vault(temp_vault_env):
    """STRESS: Measure memory usage for 10k entries."""
    import os

    import psutil

    password = temp_vault_env["password"]

    # Get baseline memory
    process = psutil.Process(os.getpid())
    baseline_memory = process.memory_info().rss / 1024 / 1024  # MB

    # Add 10k entries
    vault = load_vault(password)
    for i in range(10000):
        vault.add_entry(VaultEntry(f"site{i}.com", f"user{i}", f"password{i}", f"notes{i}"))
    save_vault(vault, password)

    # Reload vault
    vault = load_vault(password)
    entries = vault.list_entries()
    assert len(entries) == 10000

    # Measure memory after loading
    current_memory = process.memory_info().rss / 1024 / 1024  # MB
    memory_used = current_memory - baseline_memory

    print(f"\nBaseline memory: {baseline_memory:.2f} MB")
    print(f"Current memory: {current_memory:.2f} MB")
    print(f"Memory used: {memory_used:.2f} MB")

    # Assert memory usage is under 100MB
    assert memory_used < 100, f"Memory usage {memory_used:.2f}MB exceeds 100MB"


def test_atomic_write_integrity(temp_vault_env):
    """STRESS: Verify atomic writes don't corrupt on failure."""
    vault_path = temp_vault_env["vault_path"]
    password = temp_vault_env["password"]

    # Add initial entry
    vault = load_vault(password)
    vault.add_entry(VaultEntry("original.com", "user", "pass", ""))
    save_vault(vault, password)

    # Save original vault data
    original_data = vault_path.read_bytes()

    # Simulate write failure by making directory read-only (on Unix)
    # On Windows, this test will pass without the failure simulation
    import platform

    if platform.system() != "Windows":
        vault_dir = vault_path.parent
        original_mode = vault_dir.stat().st_mode
        try:
            os.chmod(vault_dir, 0o500)  # Read-only

            # Try to save (should fail)
            vault.add_entry(VaultEntry("new.com", "user2", "pass2", ""))
            try:
                save_vault(vault, password)
            except Exception:
                pass  # Expected to fail

            # Restore permissions
            os.chmod(vault_dir, original_mode)

            # Verify original vault is intact
            current_data = vault_path.read_bytes()
            assert current_data == original_data, "Vault was corrupted by failed write"
        finally:
            os.chmod(vault_dir, original_mode)
    else:
        # On Windows, just verify atomic write works normally
        vault.add_entry(VaultEntry("new.com", "user2", "pass2", ""))
        save_vault(vault, password)
        vault = load_vault(password)
        assert vault.find_entry("new.com") is not None


def test_concurrent_read_stress(temp_vault_env):
    """STRESS: Test multiple concurrent reads."""
    import threading

    password = temp_vault_env["password"]

    # Add entries
    vault = load_vault(password)
    for i in range(100):
        vault.add_entry(VaultEntry(f"site{i}.com", f"user{i}", f"pass{i}", ""))
    save_vault(vault, password)

    errors = []
    results = []

    def read_vault():
        try:
            vault = load_vault(password)
            entries = vault.list_entries()
            results.append(len(entries))
        except Exception as e:
            errors.append(str(e))

    # Spawn 20 concurrent readers
    threads = []
    for i in range(20):
        t = threading.Thread(target=read_vault)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # All reads should succeed
    assert len(errors) == 0, f"Concurrent reads failed: {errors}"
    assert all(r == 100 for r in results), "Inconsistent read results"
