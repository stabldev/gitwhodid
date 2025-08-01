"""
tests.test_utils
Test file for utilility functions.
"""

from datetime import datetime, timedelta

from gitwhodid.utils import format_time


def test_format_date() -> None:
    """Test if the `format_date` function is correctly working on different dates."""
    today = datetime.now().timestamp()
    assert format_time(today) == "today"

    yesterday = (datetime.now() - timedelta(days=1)).timestamp()
    assert format_time(yesterday) == "yesterday"

    two_days_ago = (datetime.now() - timedelta(days=2)).timestamp()
    assert format_time(two_days_ago) == "2 days ago"
