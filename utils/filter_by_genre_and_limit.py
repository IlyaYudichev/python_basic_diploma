from typing import Dict, Optional, Any, List


def filtering_by_genre(search_data: Dict[str, Optional[Any]],
                       genre_required: str, result_limit: int) -> Dict[str, Optional[Any]]:
    if search_data["docs"]:
        filtered_data: List[Dict[str, Optional[Any]]] = [i_movie for i_movie in search_data["docs"] for
                                                               i_genre_name in i_movie["genres"] if
                                                               i_genre_name["name"] == genre_required]
        search_data["docs"] = filtered_data[:result_limit]
    return search_data
