from datetime import date
import peewee as pw

db = pw.SqliteDatabase("search_history.db")


class BaseModel(pw.Model):
    """
    Base class containing fields for single-row model instance of database. Parent: pw.Model.

        Attributes:
            model_id (int): primary key for single-row model instance of database
            created_at (datetime.date): date of movie search
    """
    model_id = pw.AutoField()
    created_at = pw.DateField(default=date.today())

    class Meta:
        database = db


class History(BaseModel):
    """
    Class containing fields for single-row model instance of database. Parent: BaseModel.

        Attributes:
            user_id (int): Telegram user id number
            id (int): film id from API database
            name (varchar): film name from API database
            description (Optional[str]): film description from API database
            rating (Optional[float]): film rating from API database
            year (Optional[int]): year of film release from API database
            genres (Optional[str]): film genres from API database
            ageRating (Optional[int]): age rating from API database
            poster (Optional[str]): link to film poster from API database
            is_viewed (bool): status flag whether movie has been watched or not
    """
    user_id = pw.IntegerField()
    id = pw.IntegerField()
    name = pw.CharField()
    description = pw.TextField(null=True)
    rating = pw.FloatField(null=True)
    year = pw.IntegerField(null=True)
    genres = pw.TextField(null=True)
    ageRating = pw.IntegerField(null=True)
    poster = pw.TextField(null=True)
    is_viewed = pw.BooleanField()
