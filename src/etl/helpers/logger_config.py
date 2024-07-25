import logging
from urllib import parse

from etl.config import settings
from etl.helpers.loki_handler import LokiHandler


class Logging:
    def __init__(
        self,
        service_name: str,
        loki_url: str = parse.urljoin(settings.GRAFANA_LOKI_HOST, "loki/api/v1/push"),
    ):
        self.service_name = service_name
        self.loki_url = loki_url
        self.logger: logging.Logger | None = None
        self._setup_logger()

    def _setup_logger(self):
        # Set up the logger
        self.logger = logging.getLogger(self.service_name)
        self.logger.setLevel(settings.LOG_LEVEL)

        # Set up Loki handler
        labels = {"service": self.service_name}
        loki_handler = LokiHandler(self.loki_url, labels)
        formatter = logging.Formatter(fmt=settings.LOG_FORMAT)
        loki_handler.setFormatter(formatter)

        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(settings.LOG_LEVEL)
        ch.setFormatter(formatter)

        # Add the Loki handler to the logger
        self.logger.addHandler(loki_handler)
        # add the handlers to the logger
        self.logger.addHandler(ch)

    @property
    def get_logger(self):
        return self.logger
