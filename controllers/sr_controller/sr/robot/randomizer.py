import random

# The maximum randomness which can be added in either direction
DEFAULT_RANDOM_RANGE_PERCENT = 10


def add_jitter(
    actual_value,
    min_possible,
    max_possible,
    random_range_percent=DEFAULT_RANDOM_RANGE_PERCENT,
):
    random_range = actual_value * (random_range_percent / float(100))
    new_value = actual_value + random.uniform(-random_range, random_range)
    return type(actual_value)(max(min_possible, min(new_value, max_possible)))
