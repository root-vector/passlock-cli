# Quick Start Guide

Get started with passlock-cli in 5 minutes.

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd passlock-cli

# Install
pip install -e .

# Verify installation
passlock --help
```

## First Steps

### 1. Initialize Your Vault (30 seconds)

```bash
passlock init
```

You'll be asked to create a master password. Choose a strong one - this encrypts everything.

### 2. Add Your First Password (30 seconds)

```bash
passlock add
```

Enter:
- Site: `github.com`
- Username: your GitHub username
- Password: your GitHub password
- Notes: (optional) `Personal account`

### 3. Retrieve Your Password (10 seconds)

```bash
passlock get github.com
```

The password is now in your clipboard. Paste it anywhere. It auto-clears in 15 seconds.

### 4. See All Your Passwords (10 seconds)

```bash
passlock list
```

Shows all sites and usernames (but not the passwords).

## That's It!

You now have a secure, local password manager. 

## Next Steps

- Read [EXAMPLES.md](EXAMPLES.md) for more usage patterns
- Read [SECURITY.md](SECURITY.md) to understand the security model
- Backup your vault: `passlock export --out backup.enc`

## Common Commands

```bash
passlock init              # Create new vault
passlock add               # Add/update password
passlock get <site>        # Get password (clipboard)
passlock get <site> --show # Get password (print)
passlock list              # List all entries
passlock delete <site>     # Delete entry
passlock change-master     # Change master password
passlock export --out file # Backup vault
passlock import --in file  # Restore vault
```

## Tips

- Use a strong master password (20+ characters)
- Backup regularly: `passlock export --out backup-$(date +%Y%m%d).enc`
- Keep your system secure (antivirus, updates, firewall)
- Never share your master password

## Help

```bash
passlock --help           # General help
passlock <command> --help # Command-specific help
```

## Troubleshooting

**"Vault not found"**: Run `passlock init` first

**"Invalid master password"**: Check your password, vault is not corrupted

**Clipboard not working**: Use `passlock get <site> --show` instead

## Security Note

passlock-cli stores all data locally in `~/.passlock/` with strong encryption. No network calls are made. Your passwords never leave your computer.
