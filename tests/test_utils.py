from datetime import datetime, timedelta

from gitwhodid.utils import format_time


def test_utils() -> None:
    today = datetime.now().timestamp()
    assert format_time(today) == "today"

    yesterday = (datetime.now() - timedelta(days=1)).timestamp()
    assert format_time(yesterday) == "yesterday"

    two_days_ago = (datetime.now() - timedelta(days=2)).timestamp()
    assert format_time(two_days_ago) == "2 days ago"
