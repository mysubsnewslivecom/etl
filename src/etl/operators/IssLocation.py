import logging

from config import settings
from database.PostgresConnect import PostgresConnect
from operators.models import ISSLocationModel
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.extras import DictCursor
from requests import request

logger = logging.getLogger()


class ISSLocation:
    def __init__(self) -> None:
        self.iss_location_api = settings.iss_location_api

    def get_iss_location(self):
        response = request(method="GET", url=self.iss_location_api)
        if response.status_code == 200:
            resp = response.json()
            data = ISSLocationModel(
                latitude=float(resp["iss_position"]["latitude"]),
                longitude=float(resp["iss_position"]["longitude"]),
                location_timestamp=int(resp["timestamp"]),
            )
            return data
        else:
            raise Exception("Failed to get ISS location")

    def execute_data_iss(self, data: ISSLocationModel):
        metadata = {
            "schema_name": "custom",
            "table_name": "iss_location",
            "table_fields": [
                "location_time",
                "latitude",
                "longitude",
                "response",
            ],
            "db": "system",
        }
        pgc = PostgresConnect(db=metadata["db"])
        pg_conn = pgc.connect()
        pg_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        schema_name = metadata["schema_name"]
        table_name = metadata["table_name"]

        location_time = data.location_timestamp
        latitude = data.latitude
        longitude = data.longitude

        table_fields = metadata["table_fields"]
        insert_sql = sql.SQL(
            "INSERT INTO {schema_name}.{table_name} ({fields}) VALUES ({location_time}, {latitude}, {longitude}, {response}) RETURNING id;"
        ).format(
            schema_name=sql.Identifier(schema_name),
            table_name=sql.Identifier(table_name),
            fields=sql.SQL(",").join([sql.Identifier(col) for col in table_fields]),
            location_time=sql.Literal(location_time),
            latitude=sql.Literal(latitude),
            longitude=sql.Literal(longitude),
            response=sql.Literal(data.model_dump_json()),
        )
        with pg_conn.cursor(cursor_factory=DictCursor) as cursor:
            try:
                cursor.execute(insert_sql, 42)
                return [dict(res) for res in cursor.fetchall()]
            except Exception as e:
                logger.exception(e)
            finally:
                cursor.close()
                pg_conn.close()


if __name__ == "__main__":
    iss_location = ISSLocation()
    resp = iss_location.get_iss_location()
    logger.info(resp.model_dump_json())
    logger.info(iss_location.execute_data_iss(resp))
