# Contributing to passlock-cli

Thank you for your interest in contributing!

## Development Setup

```bash
# Clone repository
git clone https://github.com/yourusername/passlock-cli.git
cd passlock-cli

# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"
```

## Running Tests

```bash
# Run all tests
pytest -v

# Run with coverage
pytest --cov=passlock

# Run specific test file
pytest tests/test_crypto.py -v
```

## Code Formatting

```bash
# Format code with Black
black passlock tests

# Check formatting
black --check passlock tests
```

## Code Quality Standards

### Type Hints

All functions must have type hints:

```python
def encrypt_data(data: bytes, password: str, salt: bytes) -> bytes:
    ...
```

### Docstrings

Public functions need docstrings explaining purpose:

```python
def derive_key(password: str, salt: bytes) -> bytes:
    """
    Derive a 32-byte encryption key from password using Argon2id.
    
    Uses Argon2id with time_cost=3, memory_cost=64MiB, parallelism=4.
    """
    ...
```

### No Secrets in Logs

Never log passwords or keys:

```python
# Good
logger.info(f"Added entry for site: {site}")

# Bad - DON'T DO THIS
logger.info(f"Password: {password}")
```

## Testing Guidelines

- All new code must have tests
- Tests should be isolated (no dependencies between tests)
- Use descriptive test names: `test_encrypt_decrypt_roundtrip`
- Aim for high coverage of critical paths

## Pull Request Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make changes and add tests
4. Format code: `black passlock tests`
5. Run tests: `pytest -v`
6. Commit with clear message: `git commit -m "feat: add feature"`
7. Push and create PR

## Commit Message Format

Use conventional commits:

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test changes
- `refactor:` - Code refactoring
- `security:` - Security improvements

## What to Contribute

### Good First Issues

- Documentation improvements
- Test coverage improvements
- Error message clarity
- Code comments

### Feature Ideas

Open an issue first to discuss:

- Password generation
- Import from other password managers
- Performance improvements

### Security

- Discuss security changes in issues first
- Provide rationale for cryptographic changes
- Include references to standards/papers

## What NOT to Contribute

- Custom cryptographic implementations (use established libraries)
- Network/cloud features (violates local-only principle)
- Breaking changes without discussion
- Code without tests
- Unformatted code

## Questions?

Open an issue with the `question` label.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
