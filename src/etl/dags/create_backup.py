import logging

import pendulum
from pathlib import Path

from airflow.decorators import dag, task
from airflow.models.connection import Connection
from airflow.models.variable import Variable
from etl.helpers.constants import AIRFLOW_DEFAULT_ARGS
from etl.helpers.utils import get_dag_id, _get_data
from airflow.configuration import AIRFLOW_HOME

logger = logging.getLogger("airflow.task")
logger.setLevel(logging.INFO)

dag_id = get_dag_id(__file__)


@dag(
    dag_id=dag_id,
    schedule=None,
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    description="A simple tutorial DAG",
    catchup=False,
    tags=["example"],
    default_args=AIRFLOW_DEFAULT_ARGS,
)
def example_task_logger():

    @task.bash
    def create_tar() -> str:
        return "tar -cvzf /tmp/secrets.tar.gz ~/workspace/secrets/"

    @task.bash
    def backup() -> str:
        date = pendulum.now().format(fmt="%Y%M%D")
        return f"rsync -avzHP --dry-run /tmp/secrets.tar.gz ~/workspace/bckup/secrets.{date}.tar.gz"

    @task.bash
    def cleanup_logs() -> str:
        return f"bash {AIRFLOW_HOME}/scripts/clean-logs"

    create_tar() >> backup() >> cleanup_logs()


example_task_logger()
