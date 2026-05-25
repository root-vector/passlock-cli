"""CLI interface for passlock-cli"""

import getpass
import logging
import shutil
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from .crypto import create_verifier, generate_salt, verify_password
from .utils import (
    atomic_write,
    copy_to_clipboard_with_timer,
    ensure_passlock_dir,
    get_salt_path,
    get_vault_path,
    get_verifier_path,
)
from .vault import VaultEntry, create_empty_vault, load_vault, save_vault

app = typer.Typer(help="Secure local password manager")
console = Console()

# BLUE TEAM: Log to stderr only, never log secrets
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
logger = logging.getLogger(__name__)


def prompt_master_password(confirm: bool = False) -> str:
    """Prompt for master password with optional confirmation."""
    password = getpass.getpass("Master password: ")
    if not password:
        console.print("[red]Password cannot be empty[/red]")
        raise typer.Exit(1)

    if confirm:
        password2 = getpass.getpass("Confirm master password: ")
        if password != password2:
            console.print("[red]Passwords do not match[/red]")
            raise typer.Exit(1)

    return password


def verify_master_password(password: str) -> bool:
    """Verify master password against stored verifier."""
    verifier_path = get_verifier_path()
    if not verifier_path.exists():
        console.print("[red]Verifier not found. Run 'passlock init' first.[/red]")
        raise typer.Exit(1)

    verifier_hash = verifier_path.read_text()
    if not verify_password(password, verifier_hash):
        console.print("[red]Invalid master password[/red]")
        raise typer.Exit(1)
    return True


@app.command()
def init():
    """Initialize a new password vault."""
    ensure_passlock_dir()

    vault_path = get_vault_path()
    if vault_path.exists():
        console.print(
            "[yellow]Vault already exists. Use 'passlock change-master' to change password.[/yellow]"
        )
        raise typer.Exit(1)

    console.print("[bold]Initialize new password vault[/bold]")
    master_password = prompt_master_password(confirm=True)

    # Generate and save salt
    salt = generate_salt()
    salt_path = get_salt_path()
    atomic_write(salt_path, salt)

    # Create verifier
    verifier_hash = create_verifier(master_password)
    verifier_path = get_verifier_path()
    atomic_write(verifier_path, verifier_hash.encode("utf-8"))

    # Create empty vault
    create_empty_vault(master_password, salt)

    console.print("[green]✓[/green] Vault initialized successfully")
    console.print(f"[dim]Location: {vault_path.parent}[/dim]")


@app.command()
def add(
    site: Optional[str] = typer.Option(None, "--site", help="Site name"),
    username: Optional[str] = typer.Option(None, "--username", help="Username"),
):
    """Add a new password entry."""
    master_password = prompt_master_password()
    verify_master_password(master_password)

    try:
        vault = load_vault(master_password)
    except Exception as e:
        console.print(f"[red]Error loading vault: {e}[/red]")
        raise typer.Exit(1)

    if site is None:
        site = typer.prompt("Site")
    if username is None:
        username = typer.prompt("Username")
    # Password must always be prompted securely
    password = getpass.getpass("Password: ")
    notes = typer.prompt("Notes (optional)", default="")

    entry = VaultEntry(site=site, username=username, password=password, notes=notes)
    vault.add_entry(entry)

    try:
        save_vault(vault, master_password)
        console.print(f"[green]✓[/green] Password saved for {site}")
    except Exception as e:
        console.print(f"[red]Error saving vault: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def get(
    site: str,
    show: bool = typer.Option(
        False, "--show", help="Print password instead of copying to clipboard"
    ),
):
    """Get a password entry."""
    master_password = prompt_master_password()
    verify_master_password(master_password)

    try:
        vault = load_vault(master_password)
    except Exception as e:
        console.print(f"[red]Error loading vault: {e}[/red]")
        raise typer.Exit(1)

    entry = vault.find_entry(site)
    if not entry:
        console.print(f"[red]No entry found for '{site}'[/red]")
        raise typer.Exit(1)

    console.print(f"[bold]{entry.site}[/bold]")
    console.print(f"Username: {entry.username}")
    if entry.notes:
        console.print(f"Notes: {entry.notes}")

    if show:
        console.print(f"Password: {entry.password}")
    else:
        copy_to_clipboard_with_timer(entry.password, timeout=15)
        console.print("[green]✓[/green] Password copied to clipboard (will clear in 15 seconds)")


@app.command()
def list():
    """List all password entries."""
    master_password = prompt_master_password()
    verify_master_password(master_password)

    try:
        vault = load_vault(master_password)
    except Exception as e:
        console.print(f"[red]Error loading vault: {e}[/red]")
        raise typer.Exit(1)

    entries = vault.list_entries()
    if not entries:
        console.print("[yellow]No entries in vault[/yellow]")
        return

    table = Table(title="Password Entries")
    table.add_column("Site", style="cyan")
    table.add_column("Username", style="green")
    table.add_column("Updated", style="dim")

    for entry in entries:
        updated = entry.updated_at[:10] if entry.updated_at else ""
        table.add_row(entry.site, entry.username, updated)

    console.print(table)
    console.print(f"\n[dim]Total: {len(entries)} entries[/dim]")


@app.command()
def delete(site: str):
    """Delete a password entry."""
    master_password = prompt_master_password()
    verify_master_password(master_password)

    try:
        vault = load_vault(master_password)
    except Exception as e:
        console.print(f"[red]Error loading vault: {e}[/red]")
        raise typer.Exit(1)

    entry = vault.find_entry(site)
    if not entry:
        console.print(f"[red]No entry found for '{site}'[/red]")
        raise typer.Exit(1)

    confirm = typer.confirm(f"Delete entry for '{entry.site}'?")
    if not confirm:
        console.print("Cancelled")
        return

    vault.delete_entry(site)

    try:
        save_vault(vault, master_password)
        console.print(f"[green]✓[/green] Entry deleted for {site}")
    except Exception as e:
        console.print(f"[red]Error saving vault: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def change_master():
    """Change the master password."""
    console.print("[bold]Change master password[/bold]")
    console.print("Enter current master password:")
    old_password = prompt_master_password()
    verify_master_password(old_password)

    try:
        vault = load_vault(old_password)
    except Exception as e:
        console.print(f"[red]Error loading vault: {e}[/red]")
        raise typer.Exit(1)

    console.print("Enter new master password:")
    new_password = prompt_master_password(confirm=True)

    # Update verifier
    verifier_hash = create_verifier(new_password)
    verifier_path = get_verifier_path()
    atomic_write(verifier_path, verifier_hash.encode("utf-8"))

    # Re-encrypt vault with new password
    try:
        save_vault(vault, new_password)
        console.print("[green]✓[/green] Master password changed successfully")
    except Exception as e:
        console.print(f"[red]Error saving vault: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def export(out: Path = typer.Option(..., "--out", help="Output file path")):
    """Export encrypted vault to a backup file."""
    vault_path = get_vault_path()
    if not vault_path.exists():
        console.print("[red]Vault not found[/red]")
        raise typer.Exit(1)

    if out.exists():
        overwrite = typer.confirm(f"File '{out}' exists. Overwrite?")
        if not overwrite:
            console.print("Cancelled")
            return

    try:
        shutil.copy2(vault_path, out)
        console.print(f"[green]✓[/green] Vault exported to {out}")
    except Exception as e:
        console.print(f"[red]Error exporting vault: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def import_vault(input_file: Path = typer.Option(..., "--in", help="Input file path")):
    """Import encrypted vault from a backup file."""
    if not input_file.exists():
        console.print(f"[red]File '{input_file}' not found[/red]")
        raise typer.Exit(1)

    console.print("[yellow]Warning: This will replace your current vault[/yellow]")
    master_password = prompt_master_password()

    # Verify the imported vault can be decrypted
    salt_path = get_salt_path()
    if not salt_path.exists():
        console.print("[red]Salt file not found. Run 'passlock init' first.[/red]")
        raise typer.Exit(1)

    try:
        import json

        from .crypto import decrypt_data

        salt = salt_path.read_bytes()
        encrypted_data = input_file.read_bytes()
        decrypted_data = decrypt_data(encrypted_data, master_password, salt)
        json.loads(decrypted_data.decode("utf-8"))  # Verify it's valid JSON
    except Exception as e:
        console.print(f"[red]Cannot decrypt vault with provided password: {e}[/red]")
        raise typer.Exit(1)

    confirm = typer.confirm("Replace current vault with imported vault?")
    if not confirm:
        console.print("Cancelled")
        return

    vault_path = get_vault_path()
    try:
        shutil.copy2(input_file, vault_path)
        console.print(f"[green]✓[/green] Vault imported successfully")
    except Exception as e:
        console.print(f"[red]Error importing vault: {e}[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
