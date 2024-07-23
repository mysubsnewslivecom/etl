from functools import cached_property
from typing import Optional
import hvac
from hvac.exceptions import VaultError

from etl.config import settings
from etl.helpers.logger_config import Logging

log = Logging(service_name=__name__).get_logger


class VaultClient:
    def __init__(
        self,
        auth_type: str = "approle",
        url: str = settings.vault_addr,
        mount_point: str = "airflow",
        role_id: str = settings.vault_approle,
        secret_id: str = settings.vault_secret_id,
        **kwargs,
    ):
        self.role_id = role_id
        self.secret_id = secret_id
        self.mount_point = mount_point
        self.kwargs = kwargs
        self.url = url
        self.auth_type = auth_type

    @property
    def client(self):
        """
        Checks that it is still authenticated to Vault and invalidates the cache if this is not the case.

        :return: Vault Client
        """
        if not self._client.is_authenticated():
            # Invalidate the cache:
            # https://github.com/pydanny/cached-property#invalidating-the-cache
            self.__dict__.pop("_client", None)
        return self._client

    @cached_property
    def _client(self) -> hvac.Client:
        """
        Return an authenticated Hashicorp Vault client.

        :return: Vault Client

        """
        _client = hvac.Client(url=self.url, **self.kwargs)
        if self.auth_type == "approle":
            self._auth_approle(_client)
        else:
            raise VaultError(f"Authentication type '{self.auth_type}' not supported")

        if _client.is_authenticated():
            return _client
        else:
            raise VaultError("Vault Authentication Error!")

    def _auth_approle(self, _client: hvac.Client):
        """
        Authenticate to Vault using AppRole.

        :param role_id: The AppRole role ID.
        :param secret_id: The AppRole secret ID.
        """
        try:
            _client.auth.approle.login(role_id=self.role_id, secret_id=self.secret_id)
            if not _client.is_authenticated():
                raise ValueError("Vault AppRole authentication failed.")
            log.info(
                "Authenticated with role-id: %s and secret-id: %s",
                self.role_id,
                self.secret_id,
            )
        except Exception as e:
            raise ValueError(f"Error during AppRole authentication: {e}")

    def read_secret(self, _path):
        """
        Read a secret from Vault.

        :param path: The path to the secret in Vault.
        :return: The secret data as a dictionary.
        """
        try:
            response = self.client.secrets.kv.v2.read_secret_version(
                path=_path,
                mount_point=self.mount_point,
                raise_on_deleted_version=True,
            )
            log.info(response["data"]["data"])
            return response["data"]["data"]
        except Exception as e:
            log.error(f"Error reading secret at {_path}: {e}")
            return None

    def write_secret(self, path, secret_data):
        """
        Write a secret to Vault.

        :param path: The path where the secret will be stored.
        :param secret_data: A dictionary of secret key-value pairs.
        :return: The response from Vault.
        """
        try:
            response = self.client.secrets.kv.v1.create_or_update_secret(
                path=path, secret=secret_data
            )
            return response
        except Exception as e:
            log.error(f"Error writing secret to {path}: {e}")
            return None

    def delete_secret(self, path):
        """
        Delete a secret from Vault.

        :param path: The path to the secret in Vault.
        :return: The response from Vault.
        """
        try:
            response = self.client.secrets.kv.v1.delete_metadata_and_all_versions(
                path=path
            )
            return response
        except Exception as e:
            log.error(f"Error deleting secret at {path}: {e}")
            return None

    def list_secrets(self, path):
        """
        List secrets at a specific path.

        :param path: The path to list secrets from.
        :return: A list of secret names.
        """
        log.info("List secrets")
        try:
            secrets = self.client.secrets.kv.v2.list_secrets(path=path)
            secret_list = secrets.get("data", {}).get("keys", [])
            log.info(secret_list)
            return secret_list
        except Exception as e:
            log.error(f"Error listing secrets at {path}: {e}")
            return None


# # Example usage
# if __name__ == "__main__":
#     vault_client = VaultClient(auth_type="approle")
#     secret_data = vault_client.read_secret("connections/airflow")
#     log.info("Secret data: %s", secret_data)
