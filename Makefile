USER:=root
HOST:=localhost
PASSWORD:=1234

.PHONY: run, sqlSetup, pyinst, frmt, fmtWin, v, clean
run: sqlSetup
	@python -OO src/main.py

sqlSetup:
	@python -OO src/sqlSetup.py


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
