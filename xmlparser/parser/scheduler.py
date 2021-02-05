import dramatiq

from typing import Union
from pathlib import Path

from xmlparser.settings import FIELDS
from xmlparser.db.db import DB

from .parser import XMLParser

db = DB()


@dramatiq.actor
def parse_files(path_to_files: Union[str, Path]):
    """
    Job for parsing files
    """
    parser = XMLParser(FIELDS)

    pathlist = Path(path_to_files).glob('**/*.xml')

    for path in pathlist:
        save_to_db(parser.parse_file(path))


def save_to_db(data: dict):
    """
    Job for saving it into db
    """
    db.save(data)
