from database.utils.CRUD import CRUDInterface
from database.common.models import db, History

db.connect()
db.create_tables([History])

db_write = CRUDInterface.create()
db_read = CRUDInterface.retrieve()
db_update = CRUDInterface.update()

if __name__ == "__main__":
    db_write()
    db_read()
    db_update()
