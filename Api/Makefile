.PHONY: run manage logs test

manage:
ifdef CMD
	python manage.py $(CMD)
else
	@echo Please, provide CMD argument
	@echo	Example: make manage -e CMD=help
endif

run:
	$(MAKE) manage -e CMD=runserver

logs:
	$(MAKE) manage CMD=log_to_mongo

test:
	pytest