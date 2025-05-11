@echo off
echo ===== Car Racing Game Vercel Deployment =====
echo.

echo Step 1: Checking for Node.js...
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Node.js is not installed or not in PATH.
    echo Please install Node.js from https://nodejs.org/
    echo and run this script again.
    pause
    exit /b
)
echo Node.js found!

echo.
echo Step 2: Installing Vercel CLI...
call npm install -g vercel
if %ERRORLEVEL% NEQ 0 (
    echo Failed to install Vercel CLI.
    pause
    exit /b
)

echo.
echo Step 3: Building the game...
python simple_deploy.py
if %ERRORLEVEL% NEQ 0 (
    echo Failed to build the game.
    pause
    exit /b
)

echo.
echo Step 4: Deploying to Vercel...
cd build\web
call vercel
if %ERRORLEVEL% NEQ 0 (
    echo Deployment failed.
    pause
    exit /b
)

echo.
echo Deployment completed successfully!
echo Your game should now be available at the URL provided by Vercel.
echo.
echo Press any key to exit...
pause