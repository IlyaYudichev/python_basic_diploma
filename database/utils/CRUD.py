from typing import List, TypeVar, Dict, Any, Optional

from peewee import ModelSelect, SqliteDatabase

from database.common.models import db

T = TypeVar("T")


def _store_data(database: db, model: T, movie_data: List[Dict]) -> None:
    """
    Add data to database.

    :param database: database
    :type database: SqliteDatabase
    :param model: instance model for operation of writing to single row of table
    :type model: TypeVar
    :param movie_data: data of movies for writing to database
    :type movie_data: List[Dict]
    """
    with database.atomic():
        model.insert_many(movie_data).execute()


def _retrieve_data(database: db, model: T, expression: Optional[bool]) -> ModelSelect:
    """
    Read and save data from database.

    :param database: database
    :type database: SqliteDatabase
    :param model: instance model for operation of reading single row of table
    :type model: TypeVar
    :param expression: required filter for database query
    :type expression: bool
    :return: response from database with dictionaries of key-value pairs
    :rtype: ModelSelect
    """
    with database.atomic():
        response = model.select().where(expression).dicts()
    return response


def _update_data(database: db, model: T, fields_to_update: Dict[str, Any], expression: Optional[bool] = None) -> None:
    """
    Update data in database.

    :param database: database
    :type database: SqliteDatabase
    :param model: instance model for operation of updating data in single row of table
    :type model: TypeVar
    :param fields_to_update: dictionary with data for updating database
    :type fields_to_update:  Dict[str, Any]
    :param expression: required filter for database query
    :type expression: bool
    """
    with database.atomic():
        model.update(**fields_to_update).where(expression).execute()


class CRUDInterface:
    @staticmethod
    def create():
        return _store_data

    @staticmethod
    def retrieve():
        return _retrieve_data

    @staticmethod
    def update():
        return _update_data


if __name__ == "__main__":
    _store_data()
    _retrieve_data()
    _update_data()
    CRUDInterface()
