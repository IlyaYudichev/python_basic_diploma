from typing import Dict, Optional, Any, Union
from api.api_site_request import api_request


def get_full_response(endpoint: str, params: Dict[str, Union[str, int, list]]) -> Dict[str, Optional[Any]]:
    """
    Get full data from all response pages.

    :param endpoint: endpoint for API request
    :type endpoint: str
    :param params: parameters of request
    :type params: Dict[str, Union[str, int, list]]
    :return: response from request to API
    :rtype: Dict[str, Optional[Any]]
    """
    response: Dict[str, Optional[Any]] = api_request(endpoint, params)
    if response["pages"] > 1:
        for _ in range(response["pages"] - 1):
            params["page"] += 1
            response_next_page: Dict[str, Optional[Any]] = api_request(endpoint, params)
            response["docs"].extend(response_next_page["docs"])
    return response
