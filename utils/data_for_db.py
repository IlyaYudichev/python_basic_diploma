from typing import List, Dict, Optional, Any, Union
from database.common.models import History


def get_data_for_db(user_id: int, response_data: List[Dict[str, Optional[Any]]]) -> List[Dict[str, Optional[Any]]]:
    """
    Get required fields to write to database.

    :param user_id: user id
    :type user_id: int
    :param response_data: movies data from API
    :type response_data: List[Dict[str, Optional[Any]]]
    :return: list of dictionaries with required fields for each movie
    :rtype: List[Dict[str, Optional[Any]]]
    """
    required_fields_list: List[Dict[str, Optional[Any]]] = []
    for i_movie in response_data:
        genres_string: str = ", ".join([i_genre["name"] for i_genre in i_movie["genres"]])
        model_existing = History.get_or_none(History.user_id == user_id, History.id == i_movie["id"])
        if model_existing:
            is_viewed_flag: bool = model_existing.is_viewed
        else:
            is_viewed_flag: bool = False
        if not i_movie.get("poster"):
            movie_poster: Optional[str] = None
        elif not i_movie["poster"].get("url"):
            movie_poster: Optional[str] = None
        else:
            movie_poster: Optional[str] = i_movie["poster"]["url"]
        movie_data_dict: Dict[str, Optional[Union[int, str, bool]]] = {"user_id": user_id,
                                                                       "id": i_movie["id"],
                                                                       "name": i_movie["name"],
                                                                       "description": i_movie["description"],
                                                                       "rating": round(i_movie["rating"]["kp"], 1),
                                                                       "year": i_movie["year"],
                                                                       "genres": genres_string,
                                                                       "ageRating": i_movie["ageRating"],
                                                                       "poster": movie_poster,
                                                                       "is_viewed": is_viewed_flag
                                                                       }
        required_fields_list.append(movie_data_dict)
    return required_fields_list
