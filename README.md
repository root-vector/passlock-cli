# passlock-cli

[![CI](https://github.com/root-vector/passlock-cli/workflows/CI/badge.svg)](https://github.com/root-vector/passlock-cli/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform: Linux](https://img.shields.io/badge/platform-linux-lightgrey.svg)](https://www.linux.org/)
[![Security: Audited](https://img.shields.io/badge/security-audited-green.svg)](SECURITY_AUDIT.md)

**Local-only encrypted password manager for terminal users**

![Demo](docs/demo.gif)

## Features

| Feature | Description |
|---------|-------------|
| **Local Only** | All data stored in `~/.passlock/`, zero network calls |
| **Argon2id** | Memory-hard key derivation (time_cost=3, memory_cost=64MiB, parallelism=4) |
| **Fernet** | AES-128-CBC + HMAC-SHA256 authenticated encryption |
| **Clipboard Auto-Clear** | Passwords clear from clipboard after 15 seconds |
| **Atomic Writes** | Vault updates use atomic operations to prevent corruption |
| **Secure Permissions** | All files created with mode 0o600 (owner read/write only) |

## Quick Start

### Install

```bash
git clone https://github.com/root-vector/passlock-cli.git
cd passlock-cli
pip install -e .
```

### Basic Usage

```bash
# Initialize vault
passlock init

# Add password
passlock add

# Get password (copies to clipboard)
passlock get github.com

# List all entries
passlock list
```

## Commands

```bash
passlock init              # Create new vault with master password
passlock add               # Add or update password entry
passlock get <site>        # Get password (clipboard, clears in 15s)
passlock get <site> --show # Get password (print to screen)
passlock list              # List all entries (no passwords shown)
passlock delete <site>     # Delete entry
passlock change-master     # Change master password
passlock export --out file # Backup encrypted vault
passlock import --in file  # Restore encrypted vault
```

## Security Model

### What IS Protected

- **Encryption at Rest**: Vault encrypted with Fernet (AES-128-CBC + HMAC-SHA256)
- **Key Derivation**: Master password → Argon2id → 32-byte key
  - `time_cost=3` (iterations)
  - `memory_cost=65536` (64 MiB)
  - `parallelism=4` (threads)
- **Salt**: 16-byte cryptographically random salt stored in `~/.passlock/salt.bin`
- **Verifier**: Argon2id hash of master password (not the password itself) stored in `~/.passlock/verifier`
- **File Permissions**: All files mode 0o600, directory mode 0o700
- **Atomic Operations**: Vault writes use temp file + atomic rename

### What IS NOT Protected

- **Keyloggers**: Malware can capture master password during entry
- **Memory Dumps**: Decrypted vault held in process memory
- **Physical Access**: Unlocked system allows vault access
- **Compromised Master Password**: If master password is known, all passwords accessible
- **Side-Channel Attacks**: Not designed for hostile multi-tenant environments

### Storage

```
~/.passlock/
├── salt.bin    # 16-byte random salt (mode 0o600)
├── verifier    # Argon2id hash of master password (mode 0o600)
└── vault.enc   # Encrypted JSON vault (mode 0o600)
```

Vault structure (encrypted):
```json
{
  "version": 1,
  "entries": [
    {
      "site": "example.com",
      "username": "user@example.com",
      "password": "secret",
      "notes": "optional notes",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

## Ethics Note

**Built for learning defensive security. Use only on systems you own.**

This tool is designed for managing your own passwords on systems you control. Do not use it to store unauthorized credentials or for any malicious purposes. The authors are not responsible for misuse.

## Development

### Run Tests

```bash
pytest -v
```

### Format Code

```bash
black passlock tests
```

### Generate Demo GIF

```bash
bash scripts/make_demo.sh
```

## Roadmap

- [ ] Password generation with configurable strength
- [ ] Import from other password managers (1Password, LastPass, Bitwarden)
- [ ] TOTP/2FA code generation

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

## Security Disclosure

Found a vulnerability? Email security@example.com (see [SECURITY.md](SECURITY.md))

## License

MIT License - See [LICENSE](LICENSE) for details.

## Project Structure

```
passlock-cli/
├── passlock/          # Main package
│   ├── cli.py         # Typer CLI commands
│   ├── crypto.py      # Argon2id + Fernet
│   ├── vault.py       # Vault operations
│   └── utils.py       # Helpers
├── tests/             # Test suite (29 tests)
├── docs/              # Documentation
└── scripts/           # Helper scripts
```

## Acknowledgments

- [cryptography](https://cryptography.io/) - Fernet implementation
- [argon2-cffi](https://github.com/hynek/argon2-cffi) - Argon2id bindings
- [Typer](https://typer.tiangolo.com/) - CLI framework
- [Rich](https://rich.readthedocs.io/) - Terminal formatting
