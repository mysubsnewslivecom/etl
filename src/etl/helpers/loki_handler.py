import json
import logging
import socket
from datetime import datetime, timezone

import requests
from requests import Response


class LokiHandler(logging.Handler):
    def __init__(self, url: str, labels: dict):
        super().__init__()
        self.url = url
        self.labels = labels

    @staticmethod
    def _get_hostname():
        return socket.gethostname()

    def _get_api_headers(self) -> dict[str, str]:
        return {
            "Content-Type": "application/json",
        }

    def _create_payload(self, log_entry):
        return {
            "streams": [
                {
                    "stream": self.labels,
                    "values": [
                        [
                            str(int(datetime.now(timezone.utc).timestamp() * 1e9)),
                            log_entry,
                        ]
                    ],
                }
            ]
        }

    def emit(self, record):
        log_entry = self.format(record)
        headers = self._get_api_headers()

        self.labels["job"] = "test-job"
        self.labels["host"] = self._get_hostname()

        payload = self._create_payload(log_entry=log_entry)

        response: Response
        try:
            response = requests.post(
                self.url, headers=headers, data=json.dumps(payload)
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except socket.gaierror as e:
            print(f"Error sending log to Loki: {e.strerror}")
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)
