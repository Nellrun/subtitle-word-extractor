# Имя виртуального окружения
VENV := venv

# Определение путей к Python и pip в виртуальном окружении
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

# Команды Makefile
.PHONY: all install

# Установка виртуального окружения и зависимостей
install: $(VENV)/bin/activate

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt
	touch $(VENV)/bin/activate
