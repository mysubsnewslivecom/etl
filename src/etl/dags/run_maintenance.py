import logging

import pendulum

from airflow.decorators import dag, task, task_group
from etl.helpers.constants import AIRFLOW_DEFAULT_ARGS
from etl.helpers.utils import get_dag_id
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
    max_active_runs=1,
    max_active_tasks=1,
    tags=["maintenance"],
    default_args=AIRFLOW_DEFAULT_ARGS,
)
def run_maintenance():

    @task.bash(task_id="cleanup-logs")
    def cleanup_logs() -> str:
        return f"bash {AIRFLOW_HOME}/scripts/clean-logs"

    @task_group(group_id="Create Backup")
    def group_backup():

        @task.bash(task_id="create-tar")
        def task_create_tar() -> str:
            return "tar -cvzf /tmp/secrets.tar.gz ~/workspace/secrets/"

        @task.bash(task_id="backup")
        def task_backup() -> str:
            date = pendulum.now().format(fmt="%Y%M%D")
            return f"rsync -avzHP --dry-run /tmp/secrets.tar.gz ~/workspace/bckup/secrets.{date}.tar.gz"

        task_create_tar() >> task_backup()

    group_backup >> cleanup_logs()


run_maintenance()
