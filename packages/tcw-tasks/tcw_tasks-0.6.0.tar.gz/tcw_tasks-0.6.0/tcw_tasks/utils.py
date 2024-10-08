import datetime
from sqlalchemy import select, func, or_
from tcw.database import session
from tcw.apps.contest.models import Contest, Entrant


def expired_contests():
    """
    Get list of contests whose time has expired, or has reached max number
    of entrants.
    """

    now = datetime.datetime.utcnow()

    #  subq = select(func.count(Contest.entrants)).where(
    #    Contest.id == Entrant.contest_id).scalar_subquery()

    # contests = session.query(Contest).filter(
    #    or_( Contest.expires < now, subq >= Contest.max_entrants )
    # ).all()

    contests = session.query(Contest).filter(Contest.expires < now).all()
    if contests is None or len(contests) == 0:
        raise Exception("No contests that meet criteria")

    return contests
