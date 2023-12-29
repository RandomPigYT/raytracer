USER:=root
HOST:=localhost
PASSWORD:=1234

run:
	mysql -h $(HOST) -u $(USER) -p < ./sqlSetup.sql
	@python -OO src/main.py

pyinst:
	@pyi-makespec.exe .\src\main.py --paths ./c_extension/lib --paths C:\Users\HP\AppData\Local\Programs\Python\Python310\Lib\site-packages\glfw --onefile
	@pyinstaller main.spec

frmt:
	@python -m black $(shell find ./src -type f -name "*.py")

fmtWin:
	@python -m black $(dir /s /b ".\src\*.py")

v:
	source ./venv/bin/activate

clean:
	@rm main.build main.dist -rf
