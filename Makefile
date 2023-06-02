ifeq ($(OS),Windows_NT)
SHELL=powershell.exe
RUN=.\scripts\Run.ps1 | more
INIT=.\scripts\Init.ps1 | more
else
SHELL=/bin/bash
RUN=./scripts/run.sh
INIT=./scripts/init.sh
endif

run: venv
	$(RUN)

venv:
	$(INIT)
