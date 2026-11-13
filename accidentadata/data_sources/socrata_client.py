import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class SocrataError(Exception):
    pass


class SocrataClient:
    BASE_URL = "https://www.datos.gov.co/resource"

    def __init__(self, app_token=None, timeout=30):
        self.app_token = app_token or os.getenv("SOCRATA_APP_TOKEN")
        self.timeout = timeout

    def fetch(self, dataset_id, limit=100, offset=0, filters=None):
        if not dataset_id or len(dataset_id) != 9 or dataset_id[4] != "-":
            raise ValueError("El identificador del conjunto de datos no es válido.")

        if not isinstance(limit, int) or limit < 1 or limit > 50000:
            raise ValueError("El límite debe estar entre 1 y 50000.")

        if not isinstance(offset, int) or offset < 0:
            raise ValueError("El desplazamiento no puede ser negativo.")

        params = {"$limit": limit, "$offset": offset}
        if filters:
            params.update(filters)

        url = f"{self.BASE_URL}/{dataset_id}.json?{urlencode(params)}"
        headers = {"Accept": "application/json"}
        if self.app_token:
            headers["X-App-Token"] = self.app_token

        request = Request(url, headers=headers)

        try:
            with urlopen(request, timeout=self.timeout) as response:
                payload = response.read().decode("utf-8")
            data = json.loads(payload)
        except HTTPError as error:
            raise SocrataError(
                f"datos.gov.co respondió con HTTP {error.code}."
            ) from error
        except URLError as error:
            raise SocrataError(
                "No fue posible conectar con datos.gov.co."
            ) from error
        except json.JSONDecodeError as error:
            raise SocrataError(
                "La respuesta de datos.gov.co no contiene JSON válido."
            ) from error

        if not isinstance(data, list):
            raise SocrataError("La respuesta recibida no tiene el formato esperado.")

        return data
