"""Core functionalities."""

MIN_LENGTH = 9


def buy(random_string):
    """Decide whether to buy or not.

    Args:
        random_string (str): a random~ish product name.

    Returns:
        boolean: Should you buy or stay.
    """
    ret = False
    if len(random_string) <= MIN_LENGTH:
        ret = True
    return ret
