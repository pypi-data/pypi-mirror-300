import math
import uuid
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence, Tuple, cast
from html import unescape

from pararamio._types import FormatterT
from pararamio.constants import DATETIME_FORMAT
from pararamio.exceptions import PararamioValidationException


__all__ = (
    'encode_digit',
    'lazy_loader',
    'encode_chat_id',
    'join_ids',
    'parse_datetime',
    'parse_iso_datetime',
    'check_login_opts',
    'get_empty_vars',
    'unescape_dict',
    'get_formatted_attr_or_load',
    'format_or_none',
    'get_utc',
    'format_datetime',
)


def check_login_opts(login: Optional[str], password: Optional[str]) -> bool:
    return all(map(bool, [login, password]))


def get_empty_vars(**kwargs: Any):
    return ', '.join([k for k, v in kwargs.items() if not v])


def encode_digit(digit: int, res: str = '') -> str:
    if not isinstance(digit, int):
        digit = int(digit)
    code_string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_.'
    result = math.floor(digit / len(code_string))
    res = code_string[int(digit % len(code_string))] + res
    return encode_digit(result, res) if result > 0 else res


def encode_chat_id(chat_id: int, posts_count: int, last_read_post_no: int) -> str:
    return '-'.join(map(str, [chat_id, posts_count, last_read_post_no]))


def encode_chats_ids(chats_ids: List[Tuple[int, int, int]]) -> str:
    return '/'.join(map(lambda *args: encode_chat_id(*args), chats_ids))


def lazy_loader(cls: Any, items: Sequence, load_fn: Callable[[Any, List], List], per_load: int = 50) -> Iterable:
    load_counter = 0
    loaded_items: List[Any] = []
    counter = 0

    def load_items():
        return load_fn(cls, items[(per_load * load_counter): (per_load * load_counter) + per_load])

    for _ in items:
        if not loaded_items:
            loaded_items = load_items()
        if counter >= per_load:
            counter = 0
            load_counter += 1
            loaded_items = load_items()
        yield loaded_items[counter]
        counter += 1


def join_ids(items: List[Any]) -> str:
    return ','.join(map(str, items))


def get_utc(date: datetime) -> datetime:
    if date.tzinfo is None:
        raise PararamioValidationException('is not offset-aware datetime')
    return cast(datetime, date - cast(timedelta, date.utcoffset()))


def parse_datetime(data: Dict[str, Any], key: str, format_: str = DATETIME_FORMAT) -> Optional[datetime]:
    if key not in data:
        return None
    return datetime.strptime(data[key], format_).replace(tzinfo=timezone.utc)


def parse_iso_datetime(data: Dict[str, Any], key: str) -> Optional[datetime]:
    try:
        return parse_datetime(data, key, '%Y-%m-%dT%H:%M:%S.%fZ')
    except ValueError:
        return parse_datetime(data, key, '%Y-%m-%dT%H:%M:%SZ')


def format_datetime(date: datetime) -> str:
    return get_utc(date).strftime(DATETIME_FORMAT)


def rand_id():
    _hash = hashlib.md5(bytes(uuid.uuid4().hex, 'utf8'))
    return str(int(int(_hash.hexdigest(), 16) * 10 ** -21))


def unescape_dict(d: Dict[str, Any], keys: List[str]) -> Dict[str, Any]:
    """
    Unescapes the html values of specified keys in a dictionary.

    :param d: The dictionary whose values are to be unescaped.
    :type d: Dict[str, Any]
    :param keys: The list of keys whose corresponding values in the dictionary are to be unescaped.
    :type keys: List[str]
    :return: A dictionary with the values of specified keys unescaped (other values remain unchanged).
    :rtype: Dict[str, Any]
    """
    return {k: unescape(v) if k in keys else v for k, v in d.items()}

def format_or_none(key: str, data: Dict[str, Any], formatter: Optional[FormatterT]) -> Any:
    if formatter is not None and key in formatter:
        return formatter[key](data, key)
    return data[key]

def get_formatted_attr_or_load(obj: object, key: str, formatter: Optional[FormatterT] = None, load_fn: Optional[Callable[[], Any]] = None) -> Any:
    try:
        return format_or_none(key, getattr(obj, '_data', {}), formatter)
    except KeyError:
        if load_fn is not None:
            load_fn()
            return format_or_none(key, getattr(obj, '_data', {}), formatter)
        raise
