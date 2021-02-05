import json

from bottle import route, run, request
from xmlparser.db.db import DB
from xmlparser.settings import (
    PAGE_SIZE,
    HOST,
    PORT,
    DEBUG
)

db = DB()


@route("/info/<page:int>")  # will fail if number of page overflow int size, better to use cursor
def show_data(page):
    """
    Show extracted data
    """
    sort_by = request.query.sort_by
    offset = (page-1) * PAGE_SIZE
    result = db.fetch(offset, sort_by)
    print(result)
    return {'items': result}


run(host='localhost', port=8080, debug=True)
