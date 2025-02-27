include .env

define HELP_BODY

*************************
* Makefile Command Help *
*************************

Configuração:
  make build-image
  make debug
  make debug-stop
  make init-database
  make update-all
  make update
  make run
  make stop

endef

export HELP_BODY
ls:
	@echo "$$HELP_BODY"
list: ls

build-image:
	cd ./build/odoo && \
	docker build -t odoo:development-v18 . && \
	cd ../../

configure:
	COMMAND=odoo \
	UPDATE=Y \
	MODULES=all \
	INIT_DATABASE=Y \
	docker compose --file=docker-compose.yml up

debug:
	COMMAND=debug \
	UPDATE=N \
	MODULES= \
	INIT_DATABASE=N \
	docker compose --file=docker-compose-debug-vscode.yml up -d && sleep 5

debug-stop:
	docker compose --file=docker-compose-debug-vscode.yml stop

init-database:
	COMMAND=odoo \
	UPDATE=N \
	MODULES= \
	INIT_DATABASE=Y \
	docker compose --file=docker-compose-debug-vscode.yml up

update-all:
	COMMAND=odoo \
	UPDATE=Y \
	MODULES=all \
	INIT_DATABASE=N \
	docker compose --file=docker-compose-debug-vscode.yml up

update:
	COMMAND=odoo \
	UPDATE=Y \
	MODULES=odoo_sample_module \
	INIT_DATABASE=N \
	docker compose --file=docker-compose-debug-vscode.yml up

run:
	docker compose --file=docker-compose.yml up

stop:
	docker compose --file=docker-compose-debug-vscode.yml stop
