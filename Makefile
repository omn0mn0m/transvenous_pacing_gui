# Help target from https://gist.github.com/prwhite/8168133

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'

# =================================== 
# Make Targets
# =================================== 
help:			## Show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:		## Installs Python dependencies using pip
	pip install -r requirements.txt

test:			## Runs the unit tests for this project
	pytest --cov-config .coveragerc --cov=transvenous_pacing_gui tests/

complexity:		## Runs a complexity report using lizard and checks for overly complex code
	lizard

build:			## Builds the project for pypi distribution
	python setup.py sdist

upload-test:	## Uploads the project distribution to pypi test server
upload-test: build
	twine upload .\dist\* -r testpypi

upload: build	## Uploads the project distribution to pypi production server
	twine upload .\dist\*

clean:			## Cleans the project of generated files
	rm -rf ./dist

.PHONY: init test complexity build upload-test upload clean
