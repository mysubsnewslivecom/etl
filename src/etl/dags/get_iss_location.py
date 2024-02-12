from __future__ import annotations

import os
import sys
import json

import pendulum

from airflow.decorators import dag, task

libpath = os.path.abspath("src/etl")
sys.path.append(libpath)

from operators.IssLocation import ISSLocation


@dag(
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["example"],
)
def get_iss_location():

    @task()
    def get_data():
        iss_location = ISSLocation()
        data = iss_location.get_iss_location()
        return iss_location.execute_data_iss(data=data)

    get_data()


get_iss_location()
