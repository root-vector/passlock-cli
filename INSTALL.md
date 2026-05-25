# Installation Guide

Complete installation and verification guide for passlock-cli.

## System Requirements

- **Python**: 3.11 or higher
- **Operating System**: Windows, macOS, or Linux
- **pip**: Latest version recommended

## Installation Methods

### Method 1: Install from Source (Recommended)

```bash
# 1. Clone the repository
git clone <repository-url>
cd passlock-cli

# 2. (Optional) Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install in editable mode
pip install -e .

# 4. Verify installation
passlock --help
```

### Method 2: Install with Development Dependencies

```bash
# Install with dev dependencies (for contributors)
pip install -e ".[dev]"

# Verify
passlock --help
pytest
black --check passlock tests
```

### Method 3: Direct Dependency Installation

```bash
# Install dependencies manually
pip install typer rich cryptography argon2-cffi pyperclip

# Then install passlock-cli
pip install -e .
```

## Verification

### 1. Check Installation

```bash
$ passlock --help
```

Expected output:
```
Usage: passlock [OPTIONS] COMMAND [ARGS]...

Secure local password manager

Commands:
  init           Initialize a new password vault.
  add            Add a new password entry.
  get            Get a password entry.
  list           List all password entries.
  delete         Delete a password entry.
  change-master  Change the master password.
  export         Export encrypted vault to a backup file.
  import-vault   Import encrypted vault from a backup file.
```

### 2. Run Tests

```bash
$ pytest -v
```

Expected: All 29 tests pass

### 3. Check Code Formatting

```bash
$ black --check passlock tests
```

Expected: "All done! ✨ 🍰 ✨"

### 4. Test Basic Workflow

```bash
# Initialize vault
$ passlock init
Master password: [enter password]
Confirm master password: [enter password]
✓ Vault initialized successfully

# Add entry
$ passlock add
Master password: [enter password]
Site: test.com
Username: user@test.com
Password: [enter password]
Notes (optional): Test entry
✓ Password saved for test.com

# List entries
$ passlock list
Master password: [enter password]
[Shows table with test.com entry]

# Get entry
$ passlock get test.com
Master password: [enter password]
test.com
Username: user@test.com
✓ Password copied to clipboard

# Clean up
$ rm -rf ~/.passlock  # On Windows: rmdir /s /q %USERPROFILE%\.passlock
```

## Platform-Specific Notes

### Windows

```cmd
# Install
pip install -e .

# Verify
passlock --help

# Vault location
%USERPROFILE%\.passlock\
```

### macOS

```bash
# Install
pip3 install -e .

# Verify
passlock --help

# Vault location
~/.passlock/

# Note: Clipboard requires pyperclip with pasteboard support
```

### Linux

```bash
# Install
pip3 install -e .

# Verify
passlock --help

# Vault location
~/.passlock/

# Note: Clipboard may require xclip or xsel
sudo apt-get install xclip  # Debian/Ubuntu
sudo yum install xclip      # RHEL/CentOS
```

## Troubleshooting

### "command not found: passlock"

**Cause**: pip install directory not in PATH

**Solution**:
```bash
# Find pip install location
python -m site --user-base

# Add to PATH (add to ~/.bashrc or ~/.zshrc)
export PATH="$PATH:$(python -m site --user-base)/bin"
```

### "No module named 'passlock'"

**Cause**: Not installed or wrong Python environment

**Solution**:
```bash
# Ensure you're in the right environment
which python
python --version

# Reinstall
pip install -e .
```

### "Permission denied" on ~/.passlock

**Cause**: Incorrect file permissions

**Solution**:
```bash
# Fix permissions (Unix/Linux/macOS)
chmod 700 ~/.passlock
chmod 600 ~/.passlock/*
```

### Clipboard not working

**Cause**: Missing clipboard dependencies

**Solution**:

**Linux**:
```bash
sudo apt-get install xclip  # or xsel
```

**macOS**: Should work out of the box

**Windows**: Should work out of the box

**Workaround**: Use `--show` flag
```bash
passlock get site.com --show
```

### Tests failing

**Cause**: Missing dev dependencies

**Solution**:
```bash
pip install pytest black
```

### Import errors

**Cause**: Dependency version conflicts

**Solution**:
```bash
# Create fresh virtual environment
python -m venv fresh_venv
source fresh_venv/bin/activate
pip install -e .
```

## Upgrading

### From Source

```bash
cd passlock-cli
git pull
pip install -e . --upgrade
```

### Verify Upgrade

```bash
passlock --help
pytest -v
```

## Uninstallation

### Remove Package

```bash
pip uninstall passlock-cli
```

### Remove Data (Optional)

```bash
# CAUTION: This deletes all your passwords!

# Backup first
passlock export --out backup.enc

# Then remove
rm -rf ~/.passlock  # Unix/Linux/macOS
rmdir /s /q %USERPROFILE%\.passlock  # Windows
```

## Virtual Environment Setup

### Why Use Virtual Environments?

- Isolate dependencies
- Avoid conflicts with system packages
- Easy to recreate

### Create Virtual Environment

```bash
# Create
python -m venv passlock-env

# Activate
source passlock-env/bin/activate  # Unix/Linux/macOS
passlock-env\Scripts\activate     # Windows

# Install
pip install -e .

# Deactivate when done
deactivate
```

## Docker Installation (Advanced)

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install -e .

ENTRYPOINT ["passlock"]
```

```bash
# Build
docker build -t passlock-cli .

# Run
docker run -it -v ~/.passlock:/root/.passlock passlock-cli
```

## Development Installation

For contributors:

```bash
# Clone
git clone <repository-url>
cd passlock-cli

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install with dev dependencies
pip install -e ".[dev]"

# Verify
pytest -v
black --check passlock tests
passlock --help
```

## Verification Checklist

- [ ] `passlock --help` shows all commands
- [ ] `pytest -v` shows 29 tests passing
- [ ] `black --check passlock tests` passes
- [ ] `passlock init` creates ~/.passlock/
- [ ] `passlock add` successfully adds entry
- [ ] `passlock get` copies to clipboard
- [ ] `passlock list` shows entries
- [ ] File permissions are 0o600 (Unix/Linux/macOS)

## Getting Help

- **Documentation**: See README.md, QUICKSTART.md, EXAMPLES.md
- **Issues**: Open an issue on GitHub
- **Security**: Email maintainers directly (see SECURITY.md)

## Next Steps

After successful installation:

1. Read [QUICKSTART.md](QUICKSTART.md) for basic usage
2. Read [EXAMPLES.md](EXAMPLES.md) for detailed examples
3. Read [SECURITY.md](SECURITY.md) to understand security model
4. Backup regularly: `passlock export --out backup.enc`
