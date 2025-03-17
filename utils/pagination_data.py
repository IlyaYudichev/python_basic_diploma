from typing import List, Dict, Optional, Tuple, Any

URL_NO_POSTER: str = "https://avatars.mds.yandex.net/get-mpic/5233098/img_id5363138375069804171.jpeg/orig"


def get_pagination_data(movies_data: List[Dict[str, Optional[Any]]], history_flag: bool = False) -> Tuple[
    List[str], List[str]]:
    """
    Get data for movie paginator.

    :param movies_data: movies data from API
    :type movies_data: List[[str, Optional[Any]]]
    :param history_flag: flag for pagination of 'history' type
    :type history_flag: bool
    :return: data for movie paginator
    :rtype: Tuple[List[str], List[str]]
    """
    movies_pages: list = []
    for i_movie in movies_data:
        for i_key in i_movie.keys():
            if i_key == "poster":
                continue
            if i_movie[i_key] is None:
                i_movie[i_key]: str = "-"
        if "budget" in i_movie:
            budget: str = "\nБюджет: {budget_value} {budget_currency}".format(budget_value=i_movie["budget"]["value"],
                                                                              budget_currency=i_movie["budget"][
                                                                                  "currency"])
        else:
            budget: str = ""
        if history_flag:
            genres_string: str = i_movie["genres"]
            rating: float = i_movie["rating"]
            film_id: str = str(i_movie["id"]) + "#"
            if i_movie["is_viewed"]:
                is_viewed_status: str = "\nПросмотрен: да"
            else:
                is_viewed_status: str = "\nПросмотрен: нет"
        else:
            genres_string: str = ", ".join([i_genre["name"] for i_genre in i_movie["genres"]])
            rating: float = round(i_movie["rating"]["kp"], 1)
            is_viewed_status: str = ""
            film_id: str = ""
        string_template: str = "{film_id}\"{name}\"\nРейтинг: {rating}\nГод: {year}\nЖанр: {genres}\nВозраст: {ageRating}+{budget}{is_viewed_status}\n{description}".format(
            film_id=film_id,
            name=i_movie["name"],
            rating=rating,
            year=i_movie["year"],
            genres=genres_string,
            ageRating=i_movie["ageRating"],
            budget=budget,
            is_viewed_status=is_viewed_status,
            description=i_movie["description"]
        )
        result_string: str = string_template.replace("-+", "-")
        movies_pages.append(result_string)
    if history_flag:
        movies_posters: List[str] = [i_film["poster"] if i_film["poster"] else URL_NO_POSTER for i_film in
                                     movies_data]
    else:
        movies_posters: List[str] = [i_film["poster"]["url"] if i_film["poster"] else URL_NO_POSTER for i_film
                                     in
                                     movies_data]
    return movies_posters, movies_pages
