install:
	pip install -r requirements.txt

test:
	pytest --cov-config .coveragerc --cov=guiclient --cov=guiserver tests/

.PHONY: init test
