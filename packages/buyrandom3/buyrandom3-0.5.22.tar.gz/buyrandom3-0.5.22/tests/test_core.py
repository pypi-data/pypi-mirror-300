"""Unit tests for buyrandom2.core"""

import buyrandom3.core as brc


def test_buy(short_string):
    """Verify short_string is true."""
    assert brc.buy(short_string)
