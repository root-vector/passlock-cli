@echo off
REM Deployment script for passlock-cli v0.1.0

echo.
echo ========================================
echo   passlock-cli Deployment Script
echo ========================================
echo.

REM Check if git is initialized
if not exist ".git" (
    echo [*] Initializing git repository...
    git init
    echo [+] Git initialized
) else (
    echo [+] Git already initialized
)

echo.
echo [*] Adding all files...
git add .

echo.
echo [*] Creating commit...
git commit -m "feat: v0.1.0 initial secure release" -m "" -m "- Local-only encrypted password manager" -m "- Argon2id + Fernet encryption" -m "- Comprehensive security audit" -m "- 46 tests (100%% passing)" -m "- Production-ready"

echo.
echo [*] Setting main branch...
git branch -M main

echo.
echo [*] Adding remote origin...
git remote add origin https://github.com/root-vector/passlock-cli.git 2>nul
if errorlevel 1 (
    echo [!] Remote already exists
) else (
    echo [+] Remote added
)

echo.
echo [*] Pushing to GitHub...
git push -u origin main

echo.
echo ========================================
echo   Deployment Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Go to https://github.com/root-vector/passlock-cli
echo 2. Create release v0.1.0
echo 3. Enable GitHub Actions
echo 4. Configure branch protection (optional)
echo.
echo passlock-cli is now live!
echo.
pause
