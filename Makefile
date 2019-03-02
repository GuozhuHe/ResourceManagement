PYTHON:=$(shell which python3)

all: python docker

.PHONY: clean python test flake8

python: setup.py requirements.txt
	pip install virtualenv
	echo "\n Creating python virtual environment......\n"
	virtualenv -p $(PYTHON) env
	echo "\n Use python virtual environment to install required packages......\n"
	env/bin/pip install -e .

docker:
	mkdir -p ./docker_data
	docker image pull mysql:5.7
	docker image pull redis:5.0

test: flake8
	env/bin/nosetests -vd

flake8:
	env/bin/flake8

clean:
	-rm -rf env cover *eggs *.egg-info *.egg
	@find . -type f -name "*.py[co]" -delete
	@find . -type d -name "__pycache__" -delete
