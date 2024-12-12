from datetime import date
import peewee as pw

db = pw.SqliteDatabase("search_history.db")


class BaseModel(pw.Model):
    created_ad = pw.DateField(default=date.today())

    class Meta:
        database = db


class History(BaseModel):
    movie_name = pw.CharField()
    movie_description = pw.TextField()
    movie_rating = pw.CharField()
    year_of_production = pw.CharField()
    movie_genre = pw.CharField()
    age_rating = pw.CharField()
    poster = pw.BlobField()
