CALL .\.venv\Scripts\activate
pip install -r .\requirements.txt
pyinstaller .\rocketleagueminimapgenerator\main.py --onefile
pause
