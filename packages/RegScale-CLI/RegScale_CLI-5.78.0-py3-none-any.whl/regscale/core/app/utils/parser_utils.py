import logging
from typing import Any

logger = logging.getLogger(__name__)


def safe_float(value: Any, default: float = 0.0, field_name: str = "value") -> float:
    """
    Safely convert any value to a float.

    :param Any value: The value to convert
    :param float default: The default value to return if conversion fails
    :param str field_name: The name of the field being parsed (for logging purposes)
    :return: The parsed float value or the default value
    :rtype: float
    """
    if value is None:
        return default

    try:
        return float(value)
    except (ValueError, TypeError):
        logger.warning(f"Invalid float {field_name}: {value}. Defaulting to {default}")
        return default
