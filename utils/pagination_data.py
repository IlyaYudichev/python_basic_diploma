from typing import List, Dict, Optional, Tuple, Any


def get_pagination_data(movies_data: Dict[str, Optional[Any]]) -> Tuple[List[str], List[str]]:
    movies_pages: list = []
    for i_movie in movies_data["docs"]:
        genres_string: str = ", ".join([i_genre["name"] for i_genre in i_movie["genres"]])
        string_template: str = "\"{name}\"\nРейтинг: {rating}\nГод: {year}\nЖанр: {genres}\nВозраст: {ageRating}+\n{description}".format(
            name=i_movie["name"],
            rating=round(i_movie["rating"]["kp"], 1),
            year=i_movie["year"],
            genres=genres_string,
            ageRating=i_movie["ageRating"],
            description=i_movie["description"]
        )
        movies_pages.append(string_template)
    url_no_poster: str = "https://avatars.mds.yandex.net/get-mpic/5233098/img_id5363138375069804171.jpeg/orig"
    movies_posters: List[str] = [i_film["poster"]["url"] if i_film["poster"]["url"] else url_no_poster for i_film in
                                 movies_data["docs"]]
    return movies_posters, movies_pages
