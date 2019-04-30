install:
	pip install -r requirements.txt

test:
	pytest --cov-config .coveragerc --cov=guiclient --cov=guiserver tests/

complexity:
	lizard

build:
	python setup.py sdist

upload-test: build
	twine upload .\dist\* -r testpypi

upload: build
	twine upload .\dist\*

.PHONY: init test complexity
