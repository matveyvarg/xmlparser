import dramatiq
import sys

from typing import Union
from pathlib import Path

from xmlparser.settings import FIELDS
from xmlparser.db.db import DB

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

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


if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(
        parse_files.send(sys.argv[1]),
        CronTrigger.from_crontab("* * * * *"),  # TODO: Get it from settings
    )
    try:
        scheduler.start()
    except KeyboardInterrupt:
        scheduler.shutdown()