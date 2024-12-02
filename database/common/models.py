from datetime import date
import peewee as pw

db = pw.SqliteDatabase("search_history.db")


class BaseModel(pw.Model):
    created_ad = pw.DateField(default=date.today())

    class Meta:
        database = db


class History(BaseModel):
    
