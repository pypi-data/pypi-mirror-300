import os
import pprint
import re
import socket
from typing import Any, Optional, Dict, Union, Tuple
from xml.etree import ElementTree as ET

import inflect
from flask import Flask, current_app
from jinja2 import Environment, FileSystemLoader

from flarchitect.utils.config_helpers import get_config_or_model_meta
from flarchitect.utils.core_utils import convert_case, get_count
from flarchitect.utils.responses import CustomResponse

HTTP_METHODS = ["GET", "POST", "PATCH", "DELETE"]
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
html_path = ""
p = inflect.engine()


class AttributeInitializerMixin:
    """Used for the base Architect flask extension and others to initialize their config attributes."""

    def __init__(self, app: Flask, *args, **kwargs):
        self._set_class_attributes(**kwargs)
        self._set_app_config_attributes(app)
        super().__init__()

    def _set_app_config_attributes(self, app: Flask) -> None:
        """
        Sets class attributes from Flask app config if they exist.

        Args:
            app (Flask): The Flask application instance.
        """
        for key in vars(type(self)).keys():
            if key.startswith("__"):
                continue
            config_key = key.upper().lstrip("_")
            if config_key in app.config:
                setattr(self, key, app.config[config_key])

    def _set_class_attributes(self, **kwargs: Any) -> None:
        """
        Sets class attributes from keyword arguments.

        Args:
            **kwargs: Keyword arguments representing class attributes.
        """
        for key in vars(type(self)).keys():
            if key.startswith("__"):
                continue
            if key in kwargs:
                setattr(self, key, kwargs[key])



def find_html_directory(starting_directory=None):
    # If no starting directory is provided, use the directory of the current file
    if starting_directory is None:
        starting_directory = os.path.abspath(os.path.dirname(__file__))

    # Get the list of all files and directories in the current directory
    contents = os.listdir(starting_directory)

    # Check if "html" directory exists in the current directory
    if 'html' in contents and os.path.isdir(os.path.join(starting_directory, 'html')):
        return os.path.join(starting_directory, 'html')

    # If the current directory is the root directory, stop the search
    parent_directory = os.path.dirname(starting_directory)
    if starting_directory == parent_directory:
        return None

    # Recursively go one level up
    return find_html_directory(parent_directory)

def manual_render_absolute_template(absolute_template_path: str, **kwargs: Any) -> str:
    """
    Manually renders a Jinja2 template given an absolute path.

    Args:
        absolute_template_path (str): The absolute path to the template.
        **kwargs: Additional keyword arguments to pass to the template.

    Returns:
        str: The rendered template as a string.
    """

    template_folder = os.path.join(find_html_directory(), absolute_template_path)
    if template_folder.endswith(".html"):
        template_folder, template_filename = os.path.split(template_folder)

    env = Environment(loader=FileSystemLoader(template_folder))
    template = env.get_template(template_filename)
    return template.render(**kwargs)


def find_child_from_parent_dir(parent: str, child: str, current_dir: str = os.getcwd()) -> Optional[str]:
    """
    Finds the directory of a child folder within a parent directory.

    Args:
        parent (str): The name of the parent directory.
        child (str): The name of the child directory.
        current_dir (str, optional): The current directory to start the search from.

    Returns:
        Optional[str]: The path to the child directory, or None if not found.
    """
    if os.path.basename(current_dir) == parent:
        for dirname in os.listdir(current_dir):
            if dirname == child:
                return os.path.join(current_dir, dirname)

    for dirname in os.listdir(current_dir):
        if dirname.startswith(".") or dirname == "node_modules":
            continue
        child_dir_path = os.path.join(current_dir, dirname)
        if os.path.isdir(child_dir_path):
            child_dir_path = find_child_from_parent_dir(parent, child, child_dir_path)
            if child_dir_path is not None:
                return child_dir_path

    return None


def check_rate_prerequisites(service: str) -> None:
    """
    Checks if prerequisites for a specific service (e.g., Memcached, Redis) are installed.

    Args:
        service (str): The service to check prerequisites for.

    Raises:
        ImportError: If the prerequisite is not available.
    """
    back_end_spec = "or specify a cache service URI in the flask configuration with the key API_RATE_LIMIT_STORAGE_URI={URL}:{PORT}"
    if service == 'Memcached':
        try:
            import pymemcache
        except ImportError:
            raise ImportError("Memcached prerequisite not available. Please install pymemcache " + back_end_spec)
    elif service == 'Redis':
        try:
            import redis
        except ImportError:
            raise ImportError("Redis prerequisite not available. Please install redis-py " + back_end_spec)
    elif service == 'MongoDB':
        try:
            import pymongo
        except ImportError:
            raise ImportError("MongoDB prerequisite not available. Please install pymongo " + back_end_spec)


def check_rate_services() -> Optional[str]:
    """
    Checks if any supported services (Memcached, Redis, MongoDB) are running locally and returns their URI.

    Returns:
        Optional[str]: The URI of the running service, or None if no service is found.
    """
    services = {
        'Memcached': 11211,
        'Redis': 6379,
        'MongoDB': 27017,
    }
    uri = get_config_or_model_meta("API_RATE_LIMIT_STORAGE_URI", default=None)
    if uri:
        return uri

    for service, port in services.items():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        try:
            s.connect(('127.0.0.1', port))
            s.close()
            check_rate_prerequisites(service)
            if service == 'Memcached':
                return f'memcached://127.0.0.1:{port}'
            elif service == 'Redis':
                return f'redis://127.0.0.1:{port}'
            elif service == 'MongoDB':
                return f'mongodb://127.0.0.1:{port}'
        except socket.error:
            continue

    return None


def validate_flask_limiter_rate_limit_string(rate_limit_str: str) -> bool:
    """
    Validates a rate limit string for Flask-Limiter.

    Args:
        rate_limit_str (str): The rate limit string to validate.

    Returns:
        bool: True if the rate limit string is valid, False otherwise.
    """
    pattern = re.compile(r'^\d+\s+per\s+(\d+\s+)?(second|minute|hour|day|seconds|minutes|hours|days)$', re.IGNORECASE)
    return bool(pattern.match(rate_limit_str))


def search_all_keys(model: Any, key: str) -> bool:
    """Search for a specific key in all subclasses of a given model.

    Args:
        model (Any): The model class or instance to search in.
        key (str): The key to search for.

    Returns:
        bool: True if the key is found in any subclass, False otherwise.
    """
    for subclass in model.__subclasses__():
        if any(get_config_or_model_meta(key, model=subclass, method=method) for method in HTTP_METHODS):
            return True
    return False


def generate_readme_html(file_path: str, *args: Any, **kwargs: Any) -> str:
    """Generate README content from a Jinja2 template.

    Args:
        file_path (str): The path to the Jinja2 template file.
        *args (Any): Variable length argument list.
        **kwargs (Any): Arbitrary keyword arguments.

    Returns:
        str: The rendered content as a string.
    """
    template_dir, template_file = os.path.split(file_path)
    environment = Environment(loader=FileSystemLoader(os.path.abspath(template_dir)))
    template = environment.get_template(template_file)
    return template.render(*args, **kwargs)


def read_file_content(path: str) -> str:
    """Get the content of a file.

    Args:
        path (str): The path to the file.

    Returns:
        str: The content of the file.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    if os.path.exists(path):
        with open(path, "r") as file:
            return file.read()
    raise FileNotFoundError(f"{path} not found.")


def case_no_change(s: str) -> str:
    """Return the input string unchanged.

    Args:
        s (str): The input string.

    Returns:
        str: The same input string.
    """
    return s


def pretty_print_dict(d: Dict[Any, Any]) -> str:
    """Pretty print a dictionary.

    Args:
        d (Dict[Any, Any]): The dictionary to pretty print.

    Returns:
        str: The pretty-printed dictionary.
    """
    return pprint.pformat(d, indent=2)


def update_dict_if_flag_true(
    output: Dict[str, Any], flag: bool, key: str, value: Any, case_func: Any
) -> None:
    """Update a dictionary with a key-value pair if the flag is True.

    Args:
        output (Dict[str, Any]): The dictionary to update.
        flag (bool): The flag that controls whether to update.
        key (str): The key to update in the dictionary.
        value (Any): The value to associate with the key.
        case_func (Any): The function to convert the case of the key.
    """
    if flag:
        output.update({convert_case(key, case_func): value})


def make_base_dict() -> Dict[str, Any]:
    """Create a base dictionary with configuration settings.

    Returns:
        Dict[str, Any]: The base dictionary with configuration settings.
    """
    output = {"value": "..."}
    field_case = get_config_or_model_meta("API_FIELD_CASE", default="snake_case")

    config_options = [
        ("API_DUMP_DATETIME", "datetime", "2024-01-01T00:00:00.0000+00:00"),
        ("API_DUMP_VERSION", "api_version", get_config_or_model_meta("API_VERSION", default=True)),
        ("API_DUMP_STATUS_CODE", "status_code", 200),
        ("API_DUMP_RESPONSE_TIME", "response_ms", 15),
        ("API_DUMP_COUNT", "total_count", 10),
        ("API_DUMP_NULL_NEXT_URL", "next_url", "/api/example/url"),
        ("API_DUMP_NULL_PREVIOUS_URL", "previous_url", "null"),
        ("API_DUMP_NULL_ERRORS", "errors", "null", False),
    ]

    for config, key, value, *defaults in config_options:
        flag = get_config_or_model_meta(config, default=defaults[0] if defaults else True)
        update_dict_if_flag_true(output, flag, key, value, field_case)

    return output


def pluralize_last_word(converted_name: str) -> str:
    """
    Pluralize the last word of the converted name while preserving the rest of the name and its case.

    Args:
        converted_name (str): The name after case conversion.

    Returns:
        str: The name with the last word pluralized.
    """
    delimiters = {"_": "snake", "-": "kebab"}
    delimiter = next((d for d in delimiters if d in converted_name), "")

    words = converted_name.split(delimiter) if delimiter else re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?![a-z])', converted_name)
    last_word = words[-1]
    last_word_pluralized = p.plural(p.singular_noun(last_word) or last_word)

    words[-1] = last_word_pluralized
    pluralized_name = delimiter.join(words)

    if delimiters.get(delimiter) in ["screaming_snake", "screaming_kebab"]:
        pluralized_name = pluralized_name.upper()

    return pluralized_name


def normalize_key(key: str) -> str:
    """
    Converts a key to uppercase.

    Args:
        key (str): The key to be normalized.

    Returns:
        str: The normalized key.
    """
    return key.upper()

def xml_to_dict(xml_data: Union[str, bytes]) -> Dict[str, Any]:
    """
    Converts an XML string or bytes into a dictionary.
    Args:
        xml_data (Union[str, bytes]): The XML data.
    Returns:
        Dict[str, Any]: The resulting dictionary.
    """
    xml_data = xml_data.decode() if hasattr(xml_data, "decode") else xml_data

    def element_to_dict(element: ET.Element) -> Any:
        if not list(element) and (element.text is None or not element.text.strip()):
            return None
        if element.text and element.text.strip() and not list(element):
            return element.text.strip()
        result = {}
        for child in element:
            child_result = element_to_dict(child)
            if child.tag not in result:
                result[child.tag] = child_result
            else:
                if not isinstance(result[child.tag], list):
                    result[child.tag] = [result[child.tag]]
                result[child.tag].append(child_result)
        return result

    try:
        root = ET.fromstring(xml_data)
    except ET.ParseError as e:
        raise ValueError("Invalid XML data provided") from e
    return {root.tag: element_to_dict(root)}


def handle_result(result: Any) -> Tuple[int, Any, int, Optional[str], Optional[str]]:
    """Processes the result of a route function and prepares it for the standardized response."""

    #todo really not sure why this is here again. Its a relic from the past, a lot of this needs looking at.

    status_code, value, count, next_url, previous_url = HTTP_OK, result, 1, None, None

    if isinstance(result, tuple):
        status_code, result = (result[1], result[0]) if len(result) == 2 and isinstance(result[1], int) else (HTTP_OK, result)
    if isinstance(result, dict):
        value, count = result.get("query", result), get_count(result, result.get("query"))
        next_url, previous_url = result.get("next_url"), result.get("previous_url")
    elif isinstance(result, CustomResponse):
        next_url, previous_url, count = result.next_url, result.previous_url, result.count

    return status_code, value, count, next_url, previous_url


HTTP_OK = 200
HTTP_BAD_REQUEST = 400
HTTP_INTERNAL_SERVER_ERROR = 500
HTTP_UNAUTHORIZED = 401
HTTP_FORBIDDEN = 403
