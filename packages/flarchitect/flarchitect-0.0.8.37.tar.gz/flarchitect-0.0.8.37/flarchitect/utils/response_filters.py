from typing import Dict, Any

from flarchitect.utils.config_helpers import get_config_or_model_meta


def _filter_response_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Filter response data based on configuration settings.

    Args:
        data (Dict[str, Any]): The response data to be filtered.

    Returns:
        Dict[str, Any]: The filtered response data.
    """
    filters = {
        "datetime": "API_DUMP_DATETIME",
        "api_version": "API_DUMP_VERSION",
        "status_code": "API_DUMP_STATUS_CODE",
        "response_ms": "API_DUMP_RESPONSE_MS",
        "total_count": "API_DUMP_TOTAL_COUNT",
    }

    for key, config_key in filters.items():
        if key in data and not get_config_or_model_meta(config_key, default=True):
            data.pop(key)

    for key in ["next_url", "previous_url"]:
        if key in data and not data[key] and not get_config_or_model_meta(f"API_DUMP_NULL_{key.upper()}", default=True):
            data.pop(key)

    if "errors" in data and not data.get("errors") and not get_config_or_model_meta("API_DUMP_NULL_ERRORS", default=False):
        data.pop("errors")

    return data
