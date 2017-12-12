CALL .\.venv\Scripts\activate
pip install -r .\requirements.txt
pyinstaller .\rocketleagueminimapgenerator\main.py --onefile

MOVE /Y .\dist\main.exe .\dist\rocketleagueminimapgenerator.exe
COPY /Y .\README.md .\dist\README.txt
DEL /S /Q .\dist\assets
COPY /Y .\assets .\dist\assets

powershell Compress-Archive -Force -Path .\dist\rocketleagueminimapgenerator.exe, .\dist\README.txt, .\dist\assets -DestinationPath .\dist\rocketleagueminimapgenerator.zip

pause
