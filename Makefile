include .env

################################################################################
#
# Variables
#
################################################################################

ifdef DOCKER_COMPOSE_FILE_GENERAL
	DOCKER_COMPOSE_FILE_GENERAL := $(DOCKER_COMPOSE_FILE_GENERAL)
else
	DOCKER_COMPOSE_FILE_GENERAL := "docker-compose.yaml"
endif

ifdef DOCKER_COMPOSE_FILE_DEBUG
	DOCKER_COMPOSE_FILE_DEBUG := $(DOCKER_COMPOSE_FILE_DEBUG)
else
	DOCKER_COMPOSE_FILE_DEBUG := "docker-compose-debug-vscode.yaml"
endif


################################################################################
#
# Documentation and Help
#
################################################################################

define HELP_BODY

*************************
* Makefile Command Help *
*************************

Configuração:
  make build-image
  make debug
  make debug-stop
  make test
  make init-database
  make update-all
  make update
  make run
  make stop
  make remove
  make reload
  code-check repo=path-to-repo
  code-fix repo=path-to-repo

endef

export HELP_BODY


################################################################################
#
# Commands
#
################################################################################

ls:
	@echo "$$HELP_BODY"

list: ls

build-image:
	cd ./build/odoo && \
	docker build -t $(ODOO_IMAGE) . && \
	cd ../../

configure:
	COMMAND=odoo \
	ODOO_UPDATE=Y \
	ODOO_MODULES=all \
	ODOO_DATABASE_INIT=Y \
	docker compose --file=$(DOCKER_COMPOSE_FILE_GENERAL) up

debug:
	COMMAND=debug \
	ODOO_UPDATE=N \
	ODOO_MODULES= \
	ODOO_DATABASE_INIT=N \
	docker compose --file=$(DOCKER_COMPOSE_FILE_DEBUG) up -d && sleep 5

debug-stop:
	docker compose --file=$(DOCKER_COMPOSE_FILE_DEBUG) stop

test:
	COMMAND=test \
	ODOO_UPDATE=N \
	ODOO_MODULES= \
	ODOO_DATABASE_INIT=N \
	docker compose --file=$(DOCKER_COMPOSE_FILE_DEBUG) up -d && sleep 5

init-database:
	COMMAND=odoo \
	ODOO_UPDATE=N \
	ODOO_MODULES= \
	ODOO_DATABASE_INIT=Y \
	docker compose --file=$(DOCKER_COMPOSE_FILE_GENERAL) up

update-all:
	COMMAND=odoo \
	ODOO_UPDATE=Y \
	ODOO_MODULES=all \
	ODOO_DATABASE_INIT=N \
	docker compose --file=$(DOCKER_COMPOSE_FILE_DEBUG) up

update:
	COMMAND=odoo \
	ODOO_UPDATE=Y \
	ODOO_MODULES=$(ODOO_MODULES) \
	ODOO_DATABASE_INIT=N \
	docker compose --file=$(DOCKER_COMPOSE_FILE_DEBUG) up

run:
	docker compose --file=$(DOCKER_COMPOSE_FILE_GENERAL) up -d

stop:
	docker compose --file=$(DOCKER_COMPOSE_FILE_GENERAL) stop

remove:
	docker compose --file=$(DOCKER_COMPOSE_FILE_GENERAL) down

reload:
	docker compose --file=$(DOCKER_COMPOSE_FILE_GENERAL) down && docker compose --file=$(DOCKER_COMPOSE_FILE_GENERAL) up -d

# ******************************************
# Code Control
# ******************************************

.ONESHELL:
code-check:
	REPO=$(repo)
	if [ -z "$$REPO" ]; then
		echo "Erro: É necessário informar o caminho relativo para o repositório. Ex: make code-check repo=addons/modulo" >&2
		exit 1
	fi

	BASE_PATH=$(shell pwd)/$$REPO
	cd $$BASE_PATH

	echo "\e[34mBlack Check..............................................................\e[0m\e[37;44mRunning\e[0m"
	black --check .
	echo ""

	echo "\e[34mRuff Check...............................................................\e[0m\e[37;44mRunning\e[0m"
	ruff check .
	echo ""

	echo "\e[34mMypy Check...............................................................\e[0m\e[37;44mRunning\e[0m"
	MYPYPATH=src mypy --namespace-packages --explicit-package-bases .
	echo ""
	# TIP : Desabilitado temporariamente pois está detectando erros de imports
# 	echo "\e[34mPylint Check.............................................................\e[0m\e[37;44mRunning\e[0m"
# 	pylint .
# 	echo ""

.ONESHELL:
code-fix:
	REPO=$(repo)
	if [ -z "$$REPO" ]; then
		echo "Erro: É necessário informar o caminho relativo para o repositório. Ex: make code-check repo=dags/nome_do_repositorio" >&2
		exit 1
	fi

	BASE_PATH=$(shell pwd)/$$REPO
	cd $$BASE_PATH

	echo "\e[34mRuff Check...............................................................\e[0m\e[37;44mRunning\e[0m"
	ruff check . --fix
	echo ""

	echo "\e[34mBlack Check..............................................................\e[0m\e[37;44mRunning\e[0m"
	black .
	echo ""
