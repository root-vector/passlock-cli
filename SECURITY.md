# Security Policy

## Threat Model

passlock-cli is designed for **local-only password storage** on systems you control. It protects against offline attacks on encrypted vault files but does NOT protect against malware, keyloggers, or physical access to unlocked systems.

### In Scope

- Offline attacks on vault files
- Brute-force attacks on master password
- Data tampering (authenticated encryption)
- File system permission issues
- Accidental password exposure (clipboard auto-clear)

### Out of Scope

- Malware/keyloggers on your system
- Physical access to unlocked system
- Memory dumps while vault is unlocked
- Compromised master password
- Side-channel attacks in hostile environments

## Cryptographic Design

### Key Derivation

- **Algorithm**: Argon2id (RFC 9106)
- **Parameters**: time_cost=3, memory_cost=64MiB, parallelism=4
- **Output**: 32-byte key for Fernet
- **Salt**: 16-byte cryptographically random salt

### Encryption

- **Algorithm**: Fernet (AES-128-CBC + HMAC-SHA256)
- **Authentication**: HMAC prevents tampering
- **Library**: `cryptography` (industry-standard Python crypto library)

### File Security

- All files created with mode 0o600 (owner read/write only)
- Directory created with mode 0o700 (owner read/write/execute only)
- Atomic writes prevent corruption

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

**DO NOT open a public issue for security vulnerabilities.**

### How to Report

Email: **security@example.com** (replace with actual email)

Include:

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: Depends on severity (critical issues prioritized)

### Disclosure Policy

- Allow reasonable time for fix before public disclosure
- Coordinate disclosure timing with maintainers
- Credit will be given to reporters (unless anonymity requested)

## Security Best Practices for Users

### Master Password

- Use 20+ characters
- Include uppercase, lowercase, numbers, symbols
- Don't reuse from other services
- Consider using a passphrase

### System Security

- Keep OS and software updated
- Use antivirus/antimalware
- Enable firewall
- Use full-disk encryption
- Lock screen when away

### Backup Security

- Store backups in secure locations
- Encrypt backup storage (USB, cloud)
- Test backups regularly
- Keep backups offline when possible

### Operational Security

- Don't use on shared/untrusted computers
- Clear terminal history if it logs commands
- Use `get` (clipboard) instead of `--show` when possible
- Verify file permissions: `ls -la ~/.passlock/`

## Known Limitations

1. **Single User**: Designed for single-user systems
2. **No HSM Support**: Keys derived in software, not hardware
3. **No Multi-Factor**: Only master password authentication
4. **Memory Security**: Decrypted vault held in Python memory (not locked)
5. **Clipboard Security**: Clearing depends on OS support via pyperclip

## Cryptographic Libraries

- **cryptography** (v41.0.0+): [https://cryptography.io/](https://cryptography.io/)
- **argon2-cffi** (v23.0.0+): [https://github.com/hynek/argon2-cffi](https://github.com/hynek/argon2-cffi)

Both libraries are well-maintained and widely used in production systems.

## Audit History

- **v1.0.0** (2024): Initial release, no formal audit

## References

- [Argon2 RFC 9106](https://www.rfc-editor.org/rfc/rfc9106.html)
- [Fernet Specification](https://github.com/fernet/spec/blob/master/Spec.md)
- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)

## Contact

For security issues: **security@example.com**

For general questions: Open an issue on GitHub
