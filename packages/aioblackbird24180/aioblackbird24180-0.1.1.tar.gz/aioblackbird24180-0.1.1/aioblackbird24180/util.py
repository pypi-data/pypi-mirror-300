"""Utilities for aioblackbird24180."""

import json


def parse_response(response: str) -> dict:  # type: ignore[type-arg]
    """
    Parse the response.

    Parameters:
        `response`: the response to parse as string.
    """
    # Remove the leading and trailing parentheses
    response = response.strip().strip("()")
    # The status response uses single quotes, but json requires double quotes
    response = response.replace("'", '"')
    return json.loads(response)  # type: ignore[no-any-return]
