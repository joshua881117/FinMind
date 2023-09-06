from financialdata.backend.db.router import Router
from financialdata.backend.db.db import *

r = Router()


def get_db_router():
    return r

def close_conn():
    r.close_connection()
