## Description

<!-- Provide a brief description of the changes in this PR -->

## Type of Change

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Security fix

## Checklist

### Code Quality
- [ ] My code follows the style guidelines of this project (Black formatted)
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] My changes generate no new warnings

### Testing
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] All tests pass: `pytest -v`
- [ ] Code is Black formatted: `black --check passlock tests`
- [ ] No security issues: `bandit -r passlock -ll`

### Security
- [ ] I have not introduced any hardcoded secrets or passwords
- [ ] I have not weakened any security controls
- [ ] I have not exposed sensitive data in logs or error messages
- [ ] File permissions remain secure (0o600 for sensitive files)
- [ ] All user inputs are properly validated and sanitized

### Documentation
- [ ] I have updated the documentation accordingly
- [ ] I have updated CHANGELOG.md with my changes
- [ ] I have added docstrings to new functions
- [ ] README.md is updated if user-facing changes were made

### Dependencies
- [ ] I have not added unnecessary dependencies
- [ ] All new dependencies are from trusted sources
- [ ] Dependencies are pinned to specific versions in pyproject.toml

## Additional Notes

<!-- Add any additional notes, context, or screenshots here -->

## Related Issues

<!-- Link any related issues here using #issue_number -->
Closes #
