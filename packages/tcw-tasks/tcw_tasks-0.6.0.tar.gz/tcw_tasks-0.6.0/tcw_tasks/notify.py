import os
import sys
import time
import logging
import random
import datetime
import smtplib
import argparse
from sendgrid import SendGridAPIClient
from tcw.database import session, init_engine
from tcw.apps.contest.models import Fossil
from tcw_tasks.utils import expired_contests
from tcw_tasks.models import Message


# globals #
args = None
logger = logging.getLogger('tcw-tasks')


def main():
    parse_args()
    setup_logging()

    uri = os.getenv('SQLALCHEMY_DATABASE_URI', None)
    if not uri:
        logger.error('Must have SQLALCHEMY_DATABASE_URI environment var')
        sys.exit(1)

    init_engine(uri)
    logger.info("STARTING. Debug=%s" % args.debug)

    '''
    while True:
        finish_contests()
        logger.debug("Sleeping...")
        time.sleep(60)
    '''
    finish_contests()


def finish_contests():
    contests = []
    now = datetime.datetime.utcnow()

    try:
        contests = expired_contests()
        logger.info("%d contest(s) pending closure" % len(contests))
    except Exception as x:
        logger.debug(x)
        logger.debug("No contests pending closure")
        return

    for c in contests:
        try:
            winners = c.pick_winners()
            notify_owner(c, winners)
            logger.info("Owner of contest %s notified of the winners" % (c.name))

            f = Fossil(name=c.name)
            session.add(f)

            logger.info("Closing and removing contest (%s) %s" % (c.name, c.title))
            session.delete(c)
            session.commit()

        except Exception as x:
            logger.warning(x)
            session.rollback()


def notify_owner(contest, winners):
    local = not bool(os.getenv('SENDGRID_API_KEY', 0))
    msg = Message(contest=contest, winners=winners).get_message(local)
    if local:
        with smtplib.SMTP('localhost', 25) as s:
            s.send_message(msg)
    else:
        client = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        response = client.send(msg)


def setup_logging():
    level = logging.INFO

    if args.debug:
        level = logging.DEBUG

    logging.basicConfig(
        level=level,
        format='%(asctime)s|%(name)s|%(levelname)s|%(message)s'
    )


def parse_args():
    global args

    parser = argparse.ArgumentParser(
        description='TCWinners script. Handle contests and notify owners')
    parser.add_argument('-d','--debug',
        action='store_true',
        help='turn on debug messages')
    args = parser.parse_args()


if __name__ == '__main__':
    main()
