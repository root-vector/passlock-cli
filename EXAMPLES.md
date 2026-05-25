# passlock-cli Usage Examples

## Complete Workflow Example

### 1. First Time Setup

```bash
$ passlock init
Initialize new password vault
Master password: ********
Confirm master password: ********
✓ Vault initialized successfully
Location: C:\Users\username\.passlock
```

### 2. Add Your First Password

```bash
$ passlock add
Master password: ********
Site: github.com
Username: myusername@email.com
Password: ********
Notes (optional): Personal GitHub account
✓ Password saved for github.com
```

### 3. Add More Passwords

```bash
$ passlock add
Master password: ********
Site: gmail.com
Username: myemail@gmail.com
Password: ********
Notes (optional): Primary email
✓ Password saved for gmail.com

$ passlock add
Master password: ********
Site: aws.amazon.com
Username: admin
Password: ********
Notes (optional): AWS root account - use sparingly
✓ Password saved for aws.amazon.com
```

### 4. List All Entries

```bash
$ passlock list
Master password: ********

                Password Entries
┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ Site          ┃ Username             ┃ Updated    ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│ aws.amazon.com│ admin                │ 2024-01-15 │
│ github.com    │ myusername@email.com │ 2024-01-15 │
│ gmail.com     │ myemail@gmail.com    │ 2024-01-15 │
└───────────────┴──────────────────────┴────────────┘

Total: 3 entries
```

### 5. Retrieve a Password (Clipboard)

```bash
$ passlock get github.com
Master password: ********
github.com
Username: myusername@email.com
Notes: Personal GitHub account
✓ Password copied to clipboard (will clear in 15 seconds)
```

The password is now in your clipboard. Paste it where needed. After 15 seconds, the clipboard automatically clears.

### 6. Retrieve a Password (Print to Screen)

```bash
$ passlock get github.com --show
Master password: ********
github.com
Username: myusername@email.com
Notes: Personal GitHub account
Password: my_secret_password_123
```

### 7. Update an Existing Entry

Just use `add` with the same site name:

```bash
$ passlock add
Master password: ********
Site: github.com
Username: myusername@email.com
Password: ******** (new password)
Notes (optional): Personal GitHub account - updated 2024
✓ Password saved for github.com
```

### 8. Delete an Entry

```bash
$ passlock delete aws.amazon.com
Master password: ********
Delete entry for 'aws.amazon.com'? [y/N]: y
✓ Entry deleted for aws.amazon.com
```

### 9. Change Master Password

```bash
$ passlock change-master
Change master password
Enter current master password:
Master password: ********
Enter new master password:
Master password: ********
Confirm master password: ********
✓ Master password changed successfully
```

### 10. Backup Your Vault

```bash
$ passlock export --out backup-2024-01-15.enc
✓ Vault exported to backup-2024-01-15.enc
```

Store this backup file somewhere safe (USB drive, encrypted cloud storage, etc.).

### 11. Restore from Backup

```bash
$ passlock import --in backup-2024-01-15.enc
Warning: This will replace your current vault
Master password: ********
Replace current vault with imported vault? [y/N]: y
✓ Vault imported successfully
```

## Common Scenarios

### Scenario: Setting Up on a New Computer

1. Install passlock-cli: `pip install -e .`
2. Copy your backup file to the new computer
3. Initialize vault: `passlock init` (use same master password)
4. Import backup: `passlock import --in backup.enc`

### Scenario: Forgot Which Sites You Have

```bash
$ passlock list
Master password: ********
# Shows all sites without revealing passwords
```

### Scenario: Wrong Master Password

```bash
$ passlock list
Master password: ******** (wrong password)
Invalid master password
```

The vault is not corrupted - just try again with the correct password.

### Scenario: Site Name Doesn't Match Exactly

passlock uses case-insensitive matching:

```bash
$ passlock get GitHub.com
# Works the same as:
$ passlock get github.com
```

### Scenario: Multiple Accounts for Same Site

Add a distinguishing suffix:

```bash
$ passlock add
Site: gmail.com-personal
Username: personal@gmail.com
Password: ********

$ passlock add
Site: gmail.com-work
Username: work@company.com
Password: ********
```

## Security Best Practices

### DO:
- Use a strong, unique master password (20+ characters)
- Backup your vault regularly
- Store backups in secure locations
- Use `passlock get` (clipboard) instead of `--show` when possible
- Keep your system secure (antivirus, firewall, updates)

### DON'T:
- Don't share your master password
- Don't store master password in plain text anywhere
- Don't use passlock on untrusted/shared computers
- Don't commit vault files to git repositories
- Don't store the same password for multiple critical sites

## Troubleshooting

### "Vault not found" Error

```bash
$ passlock add
Vault not found. Run 'passlock init' first.
```

**Solution**: Initialize the vault first with `passlock init`

### "Invalid master password" Error

```bash
$ passlock list
Master password: ********
Invalid master password
```

**Solution**: Enter the correct master password. The vault is not corrupted.

### Clipboard Not Working

If clipboard doesn't work on your system, use the `--show` flag:

```bash
$ passlock get site.com --show
```

### Permission Denied Errors

On Unix-like systems, ensure `~/.passlock/` has correct permissions:

```bash
chmod 700 ~/.passlock
chmod 600 ~/.passlock/*
```

## Tips and Tricks

### Quick Access Pattern

For frequently accessed passwords:

```bash
# One-liner to get password
passlock get github.com

# Then paste (Ctrl+V / Cmd+V) within 15 seconds
```

### Backup Automation

Create a simple backup script:

```bash
#!/bin/bash
DATE=$(date +%Y-%m-%d)
passlock export --out ~/backups/passlock-$DATE.enc
```

### Search for Sites

```bash
# List all entries and grep for specific site
passlock list | grep -i amazon
```

### Verify Backup Before Deleting Old Vault

```bash
# Export current vault
passlock export --out test-backup.enc

# Try importing it (on a test system or after backing up current vault)
passlock import --in test-backup.enc
```
