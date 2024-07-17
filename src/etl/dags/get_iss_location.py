from __future__ import annotations

import pendulum

from airflow.decorators import dag, task
from etl.helpers.constants import AIRFLOW_DEFAULT_ARGS
from etl.helpers.utils import get_dag_id
from etl.operators.IssLocation import ISSLocation

dag_id = get_dag_id(__file__)


@dag(
    dag_id=dag_id,
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    description="Get ISS location",
    catchup=False,
    tags=["example"],
    default_args=AIRFLOW_DEFAULT_ARGS,
)
def get_iss_location():
    @task()
    def get_data():
        iss_location = ISSLocation()
        data = iss_location.get_iss_location()
        return iss_location.execute_data_iss(data=data)

    get_data()


get_iss_location()
