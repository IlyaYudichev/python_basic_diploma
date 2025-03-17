from datetime import date
import peewee as pw

db = pw.SqliteDatabase("search_history.db")


class BaseModel(pw.Model):
    model_id = pw.AutoField()
    created_ad = pw.DateField(default=date.today())

    class Meta:
        database = db


class History(BaseModel):
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
