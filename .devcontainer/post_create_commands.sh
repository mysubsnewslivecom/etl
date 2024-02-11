#!/bin/bash

pip install --upgrade pip

export AIRFLOW_HOME=~/airflow
export AIRFLOW_VERSION=2.7.3
PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
source ~/workspace/venv/venv@airflow/bin/activate && \
    pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

# export AIRFLOW_HOME=~/airflow
# export AIRFLOW_VERSION=2.7.3
# export AIRFLOW__DATABASE__SQL_ALCHEMY_CONN="postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_SERVER:$POSTGRES_PORT/$POSTGRES_DB?options=-csearch_path%3Dairflow"
# export AIRFLOW__DATABASE__SQL_ALCHEMY_CONN="postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_SERVER:$POSTGRES_PORT/$POSTGRES_DB"
# export AIRFLOW__DATABASE__SQL_ALCHEMY_SCHEMA="airflow"
# export AIRFLOW__DATABASE__SQL_ALCHEMY_CONN_SECRET=$POSTGRES_PASSWORD

eval export $(grep -v '^#' .env | xargs )

source ~/workspace/venv/venv@airflow/bin/activate && \
    airflow standalone
