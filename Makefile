.PHONY: default init lint run doc serve
PROGRAM_NAME = python
PROGRAM = src/monoshark/monoshark.py

default: init lint doc

init:	
	pip install -r requirements.txt

lint:
	black .
	pylint src

run:
	${PROGRAM_NAME} ./${PROGRAM} ${ARGS}

doc:
	mkdocs build

serve:
	mkdocs serve

all: init lint doc run