CALL .\.venv\Scripts\activate
pip install -r .\requirements.txt
pyinstaller .\rocketleagueminimapgenerator\main.py --onefile
MOVE /Y .\dist\main.exe .\dist\rocketleagueminimapgenerator.exe
COPY /Y .\README.md .\dist\README.txt
pause
