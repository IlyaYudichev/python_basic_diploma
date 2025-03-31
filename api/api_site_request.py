from typing import Dict, Union, Optional, Any, List
from logging import getLogger, WARNING
import requests
from requests import Response
from config_data.logger_config import configure_logger
from config_data.config import KINOPOISK_API_KEY

logger = getLogger(__name__)
configure_logger(level=WARNING)


def api_request(method_endswith: str,
                params: Dict[str, Union[str, int, list]]
                ) -> Union[Dict[str, Optional[Any]], List[Dict[str, str]]]:
    """
    Get response from request to API.

    :param method_endswith: endpoint for API request
    :type method_endswith: str
    :param params: parameters of request
    :type params: Dict[str, Union[str, int, list]]
    :return: response from request to API
    :rtype: Dict[str, Optional[Any]]
    """
    url: str = f"https://api.kinopoisk.dev/{method_endswith}"

    try:
        response: Response = requests.get(
            url,
            headers={"accept": "application/json",
                     "X-API-KEY": KINOPOISK_API_KEY
                     },
            params=params,
            timeout=15
        )
        if response.status_code == requests.codes.ok:
            return response.json()
    except Exception:
        logger.warning("Exception while receiving a response to a request to API", exc_info=True)
        pass
