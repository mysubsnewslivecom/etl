import logging
from airflow.decorators import dag, task
import pendulum
from etl.helpers.utils import get_dag_id
from etl.helpers.constants import AIRFLOW_DEFAULT_ARGS
from airflow.models.connection import Connection
from airflow.models.variable import Variable

logger = logging.getLogger("airflow.task")
logger.setLevel(logging.INFO)

dag_id = get_dag_id(__file__)

postgres = Connection.get_connection_from_secrets("postgres")


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
        logger.exception("raise hell")

    log_to_both()


example_task_logger()
