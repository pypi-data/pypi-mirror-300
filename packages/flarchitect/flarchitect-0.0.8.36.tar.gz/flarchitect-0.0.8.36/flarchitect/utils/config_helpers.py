from typing import Optional, Any, List

from flask import current_app, request
from marshmallow import Schema
from sqlalchemy.orm import DeclarativeBase


def get_config_or_model_meta(
    key: str,
    model: Optional[DeclarativeBase] = None,
    output_schema: Optional[Schema] = None,
    input_schema: Optional[Schema] = None,
    default: Any = None,
    allow_join: bool = False,
    method: str = "IGNORE",
    return_from_config: bool = False,
) -> Any:
    """
    Retrieves configuration or model metadata, prioritizing model metadata.

    Args:
        key (str): The key to search for in the configuration or model meta.
        model (Optional[DeclarativeBase], optional): The SQLAlchemy model.
        output_schema (Optional[Schema], optional): The Marshmallow schema for output.
        input_schema (Optional[Schema], optional): The Marshmallow schema for input.
        default (Any, optional): The default value to return if the key is not found.
        allow_join (bool, optional): Whether to allow joining of results if multiple found.
        method (str, optional): The HTTP method (e.g., 'get', 'post').
        return_from_config (bool, optional): Whether to return the object name from which the value was retrieved.

    Returns:
        Any: The value from the config or model meta, or the default value.
    """

    # from_ob = None

    def normalize_key(key: str) -> str:
        return key.lower()

    def generate_method_based_keys(base_key: str) -> List[str]:
        methods = ["get", "post", "put", "patch", "delete"]
        return [f"{meth}_{base_key}" for meth in methods if method.lower() in meth]

    def search_in_sources(sources: List[Any], keys: List[str]) -> Optional[Any]:
        out = []
        for source in sources:
            if source is not None:
                meta = getattr(source, "Meta", None)
                if meta is not None:
                    for key in keys:
                        result = getattr(meta, key, None)
                        if isinstance(result, list) and allow_join:
                            out.extend(result)
                        if result is not None:
                            return result
        if allow_join:
            return out
        return None

    def search_in_flask_config(keys: List[str]) -> Optional[Any]:
        app = current_app
        with app.app_context():  #
            for key in keys:
                conf_val = app.config.get(
                    key.upper() if "API_" in key.upper() else "API_" + key.upper()
                )
                if conf_val is not None:
                    from_ob = "config"
                    return conf_val
            return None

    normalized_key = normalize_key(key)
    method_based_keys = generate_method_based_keys(normalized_key.replace("api_", ""))

    sources = [model, output_schema, input_schema]
    keys_for_sources = method_based_keys + [
        normalized_key,
        normalize_key(key).replace("api_", ""),
    ]
    keys_for_config = method_based_keys + [normalized_key]

    sources_checks = [
        ("model", search_in_sources(sources, keys_for_sources)),
        ("config", search_in_flask_config(keys_for_config)),
        ("default", default),
    ]

    for from_ob, result in sources_checks:
        if (
            result is not None and result != [] and result != {}
        ):  # This checks both for None and empty list
            return (result, from_ob) if return_from_config else result

    return (default, "default") if return_from_config else default


def is_xml() -> bool:
    """Check if the request is for XML data.

    Returns:
        bool: True if the request is for XML, otherwise False.
    """
    accept_header = request.headers.get("Accept", "")
    content_type_header = request.headers.get("Content-Type", "")
    return any(
        header in ["application/xml", "text/xml"]
        for header in [accept_header, content_type_header]
    )
