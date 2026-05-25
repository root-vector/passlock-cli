# GitHub Release Instructions

## Create v0.1.0 Release on GitHub

The tag `v0.1.0` has been pushed to GitHub. Now create the release:

### Steps:

1. **Go to GitHub Releases**
   - Navigate to: https://github.com/root-vector/passlock-cli/releases/new

2. **Select the Tag**
   - Choose existing tag: `v0.1.0`

3. **Release Title**
   ```
   v0.1.0 - Initial Secure Release
   ```

4. **Release Description**
   Copy the content from `RELEASE_NOTES.md` or use this summary:

   ```markdown
   ## 🎉 First Production Release
   
   passlock-cli is a local-only encrypted password manager built for terminal users who value security and simplicity.
   
   ### ✨ Highlights
   
   - **8 CLI commands**: init, add, get, list, delete, change-master, export, import
   - **Argon2id + Fernet encryption**: Military-grade security
   - **46 passing tests**: 100% CI success rate
   - **Zero network calls**: All data stays local in `~/.passlock/`
   - **Clipboard auto-clear**: Passwords clear after 15 seconds
   - **Atomic writes**: Vault corruption protection
   
   ### 📦 Installation
   
   ```bash
   git clone https://github.com/root-vector/passlock-cli.git
   cd passlock-cli
   pip install -e .
   ```
   
   ### 🚀 Quick Start
   
   ```bash
   passlock init                    # Create vault
   passlock add                     # Add password
   passlock get github.com          # Get password (clipboard)
   passlock list                    # List all entries
   ```
   
   ### 🔒 Security
   
   - Argon2id key derivation (time_cost=3, memory_cost=64MiB)
   - Fernet authenticated encryption (AES-128-CBC + HMAC-SHA256)
   - Secure file permissions (0o600)
   - Input sanitization and memory protection
   - Bandit security scan: 0 high/medium issues
   
   ### 📋 Requirements
   
   - Python 3.11+
   - Linux, macOS, or Windows
   
   ### 📚 Documentation
   
   - [README](https://github.com/root-vector/passlock-cli#readme)
   - [Security Audit](https://github.com/root-vector/passlock-cli/blob/main/SECURITY_AUDIT.md)
   - [Contributing Guide](https://github.com/root-vector/passlock-cli/blob/main/CONTRIBUTING.md)
   
   ### ⚖️ License
   
   MIT License
   
   ---
   
   **Full Changelog**: https://github.com/root-vector/passlock-cli/commits/v0.1.0
   ```

5. **Set as Latest Release**
   - ✅ Check "Set as the latest release"

6. **Publish Release**
   - Click "Publish release"

### After Publishing:

The release will be available at:
- https://github.com/root-vector/passlock-cli/releases/tag/v0.1.0

Users can install directly from the release:
```bash
pip install git+https://github.com/root-vector/passlock-cli.git@v0.1.0
```

### Optional: Add Release Assets

You can attach additional files to the release:
- `passlock-cli-0.1.0.tar.gz` (source distribution)
- `passlock-cli-0.1.0-py3-none-any.whl` (wheel distribution)

To create these:
```bash
python -m build
# Files will be in dist/
```

Then upload them as release assets on GitHub.

---

## Verify Release

After publishing, verify:

1. ✅ Release appears on: https://github.com/root-vector/passlock-cli/releases
2. ✅ Tag shows in: https://github.com/root-vector/passlock-cli/tags
3. ✅ CI badge is green: https://github.com/root-vector/passlock-cli/actions
4. ✅ README displays correctly on repository homepage

## Next Steps

1. Share the release on social media (optional)
2. Add topics to repository: `password-manager`, `security`, `cli`, `encryption`, `python`
3. Consider submitting to:
   - PyPI (for `pip install passlock-cli`)
   - Homebrew (for `brew install passlock-cli`)
   - AUR (for Arch Linux users)
