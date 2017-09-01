from . import main
from datetime import datetime


@main.app_template_filter('timesince')
def timesince_filter(timestamp):
    """
    Snippet from http://flask.pocoo.org/snippets/33/
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    """
    now = datetime.utcnow()
    diff = now - timestamp
    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days / 30, "month", "months"),
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )
    for period, singular, plural in periods:
        if period:
            return "%d %s ago" % (period, singular if period == 1 else plural)
    return default
    