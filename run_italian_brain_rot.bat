@echo off
echo.
echo ===================================================
echo        ITALIAN BRAIN ROT VIDEO GENERATOR
echo ===================================================
echo.

:: Change to the script's directory
cd /d "%~dp0"
echo Current directory: %CD%

echo Running Step 1/5: Text Generation
echo ===================================================
call python "%~dp0src\generate_text.py"
if %ERRORLEVEL% neq 0 (
    echo Error in Text Generation step! Exiting...
    pause
    exit /b 1
)
echo Text Generation completed successfully.
echo.

echo Running Step 2/5: Image Generation
echo ===================================================
call python "%~dp0src\generate_image.py"
if %ERRORLEVEL% neq 0 (
    echo Error in Image Generation step! Exiting...
    pause
    exit /b 1
)
echo Image Generation completed successfully.
echo.

echo Running Step 3/5: Speech Generation
echo ===================================================
call python "%~dp0src\generate_speech.py"
if %ERRORLEVEL% neq 0 (
    echo Error in Speech Generation step! Exiting...
    pause
    exit /b 1
)
echo Speech Generation completed successfully.
echo.

echo Running Step 4/5: Video Creation
echo ===================================================
call python "%~dp0src\create_video.py"
if %ERRORLEVEL% neq 0 (
    echo Error in Video Creation step! Exiting...
    pause
    exit /b 1
)
echo Video Creation completed successfully.
echo.

echo ===================================================
echo 🎉 ALL STEPS COMPLETED SUCCESSFULLY! 🎉
echo ===================================================
echo.
echo Your Italian Brain Rot video has been created.
echo Check the 'results/videos' directory for the final video.
echo.

echo Do you want to upload the video to YouTube? (Y/N)
set /p upload_choice=
if /i "%upload_choice%"=="Y" (
    echo.
    echo Running Step 5/5: YouTube Upload
    echo ===================================================
    call python "%~dp0src\upload_to_youtube.py"
    if %ERRORLEVEL% neq 0 (
        echo Error in YouTube Upload step!
    ) else (
        echo YouTube Upload completed successfully.
    )
    echo.
)

pause 