run:
	@python src/main.py

frmt:
	@python -m black $(shell find ./src -type f -name "*.py")

fmtWin:
	@python -m black $(dir /s /b ".\src\*.py")

v:
	source ./venv/bin/activate

clean:
	@rm main.build main.dist -rf
