run:
	@python src/main.py

frmt:
	@python -m black $(shell find ./src -type f -name "*.py")

v:
	source ./venv/bin/activate
