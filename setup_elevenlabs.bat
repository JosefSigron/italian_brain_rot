@echo off
echo Italian Brain Rot - ElevenLabs TTS Setup
echo ============================================
echo.

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Setting up ElevenLabs TTS...
python src/setup_elevenlabs.py

echo.
echo Setup complete! Press any key to exit.
pause >nul
