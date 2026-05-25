# Release Notes

## v0.1.0 - Initial Secure Release (2025-01-XX)

### 🎉 First Production Release

passlock-cli is a local-only encrypted password manager built for terminal users who value security and simplicity.

### ✨ Features

**Core Functionality**
- 8 CLI commands: `init`, `add`, `get`, `list`, `delete`, `change-master`, `export`, `import`
- Local-only storage in `~/.passlock/` - zero network calls
- Interactive prompts with secure password input (getpass)
- Rich terminal UI with tables and colored output

**Security**
- **Argon2id** key derivation (time_cost=3, memory_cost=64MiB, parallelism=4)
- **Fernet** authenticated encryption (AES-128-CBC + HMAC-SHA256)
- **Secure file permissions** (0o600 for files, 0o700 for directory)
- **Atomic writes** to prevent vault corruption
- **Clipboard auto-clear** after 15 seconds
- **Input sanitization** (control character stripping, length limits)
- **Memory protection** (key wiping after use)

**Quality Assurance**
- 46 comprehensive tests (100% passing)
  - 12 cryptographic tests
  - 11 red team adversarial tests
  - 6 stress/reliability tests
  - 17 vault operation tests
- Black code formatting (100% compliant)
- Bandit security scan (0 high/medium issues)
- CI/CD with GitHub Actions

### 📦 Installation

```bash
git clone https://github.com/root-vector/passlock-cli.git
cd passlock-cli
pip install -e .
```

### 🚀 Quick Start

```bash
# Initialize vault
passlock init

# Add password
passlock add --site github.com --username myuser

# Get password (copies to clipboard)
passlock get github.com

# List all entries
passlock list
```

### 🔒 Security Model

**Protected Against:**
- Offline brute-force attacks (Argon2id)
- Data tampering (HMAC authentication)
- Vault corruption (atomic writes)
- Accidental exposure (secure permissions)

**NOT Protected Against:**
- Keyloggers on compromised systems
- Memory dumps while vault is unlocked
- Physical access to unlocked system
- Compromised master password

### 📋 Requirements

- Python 3.11+
- Linux, macOS, or Windows
- Dependencies: typer, rich, cryptography, argon2-cffi, pyperclip

### 🧪 Testing

All tests pass on Python 3.11 and 3.12:
```bash
pytest -v  # 46 passed in ~34s
```

### 📚 Documentation

- [README.md](README.md) - Quick start and features
- [SECURITY.md](SECURITY.md) - Security disclosure policy
- [SECURITY_AUDIT.md](SECURITY_AUDIT.md) - Detailed security audit
- [CONTRIBUTING.md](CONTRIBUTING.md) - Development guidelines
- [CHANGELOG.md](CHANGELOG.md) - Version history

### 🙏 Acknowledgments

Built with:
- [cryptography](https://cryptography.io/) - Fernet implementation
- [argon2-cffi](https://github.com/hynek/argon2-cffi) - Argon2id bindings
- [Typer](https://typer.tiangolo.com/) - CLI framework
- [Rich](https://rich.readthedocs.io/) - Terminal formatting

### ⚖️ License

MIT License - See [LICENSE](LICENSE) for details.

### 🔐 Ethics Note

Built for learning defensive security. Use only on systems you own. Do not use to store unauthorized credentials or for malicious purposes.

---

**Full Changelog**: https://github.com/root-vector/passlock-cli/commits/v0.1.0
