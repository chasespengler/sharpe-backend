
PROJECT_HOME := $(shell git rev-parse --show-toplevel)

.PHONY: test
test: tests/
	python3.7 -m unittest discover --start-directory $(PROJECT_HOME)/tests/
