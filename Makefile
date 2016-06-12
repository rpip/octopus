.PHONY: help clean clean-pyc lint test

help:
	@echo "clean-pyc - remove Python file artifacts"
	@echo "lint - check style with pep8"
	@echo "test - run tests quickly with the default Python"

clean: clean-pyc

clean-pyc:
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@rm -rf __pycache__

lint:
	@pep8 *.py

test: clean
	@py.test *_test.py
