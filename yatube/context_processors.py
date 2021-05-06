import datetime as dt


def year(request):
    """The function returns a variable with the current year."""
    year_now = dt.datetime.today().year
    return {
        'year': year_now
    }
