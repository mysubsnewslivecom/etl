import logging

import pendulum
from pathlib import Path

from airflow.decorators import dag, task
from airflow.models.connection import Connection
from airflow.models.variable import Variable
from etl.helpers.constants import AIRFLOW_DEFAULT_ARGS
from etl.helpers.utils import get_dag_id

logger = logging.getLogger("airflow.task")
logger.setLevel(logging.INFO)

dag_id = get_dag_id(__file__)

LOCAL_DIR = Path(__file__).parent
AIRFLOW_SOURCES_ROOT = Path(__file__).parents[3]


def get_connections(conn_id: str):
    return Connection.get_connection_from_secrets(conn_id=conn_id)


def get_variables(key: str):
    return Variable.get(key=key)


@dag(
    dag_id=dag_id,
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    description="A simple tutorial DAG",
    catchup=False,
    tags=["example"],
    default_args=AIRFLOW_DEFAULT_ARGS,
)
def example_task_logger():
    @task
    def log_to_both():
        logger.info({"test": 123})
        logger.info("test", extra={"this": "worked", "yup": "here too"})
        postgres = get_connections(conn_id="airflow")
        logger.info(postgres.host)
        logger.info(get_variables(key="date"))

    log_to_both()


example_task_logger()
