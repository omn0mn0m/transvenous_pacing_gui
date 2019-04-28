install:
	pip install -r requirements.txt

test:
	pytest --cov-config .coveragerc --cov=guiclient --cov=guiserver tests/

complexity:
	lizard

.PHONY: init test complexity
