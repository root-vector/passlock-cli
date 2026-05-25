# Changelog

All notable changes to passlock-cli will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-05-25

### Added
- Initial release of passlock-cli
- Local-only encrypted password manager for terminal users
- Argon2id key derivation (time_cost=3, memory_cost=64MiB, parallelism=4)
- Fernet encryption (AES-128-CBC + HMAC-SHA256)
- Secure file permissions (0o600 for files, 0o700 for directory)
- Atomic write operations to prevent corruption
- Clipboard auto-clear after 15 seconds
- Input validation and sanitization
- Commands: init, add, get, list, delete, change-master, export, import
- Comprehensive test suite (46 tests including red team and stress tests)
- Security audit documentation
- CI/CD pipeline with GitHub Actions

### Security
- Permission checks on vault files (Unix/Linux/macOS)
- Key wiping from memory after use
- Control character stripping from inputs
- Double-overwrite clipboard clearing
- Graceful error handling without data leaks
- No secrets in logs (stderr only)

### Documentation
- README with quick start and security model
- SECURITY_AUDIT.md with comprehensive security analysis
- CONTRIBUTING.md with development guidelines
- SECURITY.md with responsible disclosure policy
- Examples and usage documentation

[0.1.0]: https://github.com/root-vector/passlock-cli/releases/tag/v0.1.0
