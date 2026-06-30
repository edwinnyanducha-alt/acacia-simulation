@echo off
REM ============================================================
REM  deploy_to_github.bat — Push simulation_app to GitHub
REM ============================================================
echo.
echo ============================================
echo  Belgo Simulation — GitHub Deployment Script
echo ============================================
echo.

REM Check prerequisites
where git >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Git is not installed or not in PATH.
    echo Install from: https://git-scm.com/download/win
    pause
    exit /b 1
)

REM Get repo name
set /p REPO="Enter GitHub repo name (default: acacia-simulation): "
if "%REPO%"=="" set REPO=acacia-simulation

set /p USERNAME="Enter your GitHub username: "

echo.
echo Step 1: Initialize git in simulation_app/...
cd /d "%~dp0\simulation_app"
if exist .git (
    echo [OK] Git already initialized.
) else (
    git init
    echo [OK] Git initialized.
)

echo.
echo Step 2: Create .gitignore...
if not exist .gitignore (
    echo __pycache__/ > .gitignore
    echo *.pyc >> .gitignore
    echo .cache/ >> .gitignore
    echo *.pdf >> .gitignore
    echo [OK] .gitignore created.
) else (
    echo [OK] .gitignore already exists.
)

echo.
echo Step 3: Stage all files...
git add -A
echo [OK] Files staged.

echo.
echo Step 4: Create initial commit...
git commit -m "Initial commit - Belgo Strategic Simulation Web App"
echo [OK] Commit created.

echo.
echo ============================================
echo  INSTRUCTIONS — Complete these steps in browser:
echo ============================================
echo.
echo 1. Go to https://github.new  (opens a new tab)
echo 2. Repository name: %REPO%
echo 3. Description: Belgo Strategic Simulation - Kitisuru Corporate Campus
echo 4. Keep it Public (required for Streamlit Cloud free tier)
echo 5. DO NOT initialize with README, .gitignore, or license
echo 6. Click "Create repository"
echo.
echo 7. Run these two commands (GitHub will show them):
echo    git remote add origin https://github.com/%USERNAME%/%REPO%.git
echo    git branch -M main
echo    git push -u origin main
echo.
pause

echo.
echo Step 5: Final instructions for Streamlit Cloud...
echo.
echo 1. Go to https://share.streamlit.io
echo 2. Sign in with GitHub
echo 3. Click "New app"
echo 4. Select: %USERNAME%/%REPO%
echo 5. Branch: main
echo 6. Main file: app.py
echo 7. Click "Deploy!"
echo.
echo Your app will be live at: https://%REPO%.streamlit.app
echo.
pause
