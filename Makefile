SHELL=/bin/bash
# VERSION := $(shell git describe --tags)
BUILD := $(shell git rev-parse --short HEAD)
PROJECTNAME := $(shell basename "$(PWD)")
MAKEFLAGS += --silent

FORMATTING_BEGIN_GREY = \033[30;1m
FORMATTING_END = \033[0m

LOG_DIR := /tmp/airflow

LOG := @printf -- "${FORMATTING_BEGIN_GREY} ❯ %s ${FORMATTING_END}\n"

help: ## Show help message
	@clear
	$(LOG) "OPTION=<value> Usage: make [target]"
	@grep -Eh '^[a-zA-Z0-9._-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| sort \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

scheduler: ## Start Scheduler
	@nohup airflow scheduler --pid $(LOG_DIR)/scheduler.pid > $(LOG_DIR)/airflow_scheduler.log 2>&1 &

webserver: ## Start webserver
	@nohup airflow webserver --pid $(LOG_DIR)/webserver.pid > $(LOG_DIR)/airflow_webserver.log 2>&1 &

celery: ## Start celery worker
	$(LOG) "Start celery worker"
	@nohup airflow celery worker --pid $(LOG_DIR)/celery.pid > $(LOG_DIR)/airflow_celery.log 2>&1 &

kill: ## kill all airflow process
	$(LOG) "Start celery worker"
	kill -9 $(ps -ef|grep airflow| awk -F' ' '{ print $2 }')

# pkill -f -USR2 "airflow scheduler"
