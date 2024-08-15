from __future__ import annotations

import logging
import requests
import json
from typing import TYPE_CHECKING, Sequence

from airflow.models import BaseOperator
from airflow.plugins_manager import AirflowPlugin

if TYPE_CHECKING:
    from airflow.utils.context import Context


log = logging.getLogger("airflow.task")
log.setLevel(logging.DEBUG)


class RequestOperator(BaseOperator):
    template_fields: Sequence[str] = ("url", "method", "data", "params", "headers")

    def __init__(
        self,
        url: str,
        method: str,
        data: dict[str, str] = {},
        params: dict[str, str] = {},
        headers: dict[str, str] = {},
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.url = url
        self.method = method
        self.data = json.dumps(data)
        self.params = params
        self.headers = headers
        self.headers.update({"Content-Type": "application/json"})

    def execute(self, context):
        log.warning("inside execute")
        if self.method.upper() == "GET":
            resp = self._get()
        return resp

    def _get(self):
        r = requests.get(url=self.url, headers=self.headers, params=self.params)
        r.raise_for_status()
        log.info(r.json())
        return r.json()
