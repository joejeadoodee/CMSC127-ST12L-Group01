# Makefile

VENV = myenv
REQS = requirements.txt

.PHONY: run

run:
	. $(VENV)/bin/activate && pip install -r $(REQS) && python3 main.py