import sys
from http.cookiejar import CookieJar
from typing import Any, Callable, Dict, Tuple, TypeVar, Union

if sys.version_info >= (3, 8):
    from typing import TypedDict, Optional, TypeVar

    if sys.version_info >= (3, 11):
        from typing import NotRequired
        class ProfileTypeT(TypedDict):
            unique_name: str
            id: int
            info: Optional[str]
            find_strict: bool
            name: str
            is_google: bool
            two_step_enabled: bool
            has_password: bool
            phoneconfirmed: bool
            email: str
            phonenumber: NotRequired[Optional[str]]


        class TextParsedT(TypedDict):
            type: str
            value: str
            name: NotRequired[str]
            id: NotRequired[int]


        class PostMetaUserT(TypedDict):
            id: int
            name: str
            unique_name: str
            is_bot: NotRequired[bool]

    else:
        class ProfileTypeT(TypedDict):
            unique_name: str
            id: int
            info: Optional[str]
            find_strict: bool
            name: str
            is_google: bool
            two_step_enabled: bool
            has_password: bool
            phoneconfirmed: bool
            email: str
            phonenumber: Optional[str]


        class TextParsedT(TypedDict):
            type: str
            value: str
            name: Optional[str]
            id: Optional[int]


        class PostMetaUserT(TypedDict):
            id: int
            name: str
            unique_name: str
            is_bot: Optional[bool]


    class PostMetaFileT(TypedDict):
        name: str
        guid: str
        size: int
        mime_type: str
        origin: Tuple[int, int]


    class MetaReplyT(TypedDict):
        text: str
        user_id: int
        user_name: str
        in_thread_no: int


    class PostMetaThreadT(TypedDict):
        title: str


    class PostMetaT(TypedDict):
        user: PostMetaUserT
        thread: PostMetaThreadT
        file: PostMetaFileT
        reply: MetaReplyT


    class PostMention(TypedDict):
        id: int
        name: str
        value: str

else:
    ProfileTypeT = Dict[str, Any]
    PostMetaT = Dict[str, Any]
    PostMention = Dict[str, Union[str, int]]
    TextParsedT = Dict[str, Union[str, int]]
FormatterT = Dict[str, Callable[[Dict[str, Any], str], Any]]
CookieJarT = TypeVar('CookieJarT', bound=CookieJar)
QuoteRangeT = Dict[str, Union[str, int]]
HeaderLikeT = Dict[str, str]
SecondStepFnT = Callable[[CookieJar, Dict[str, str], str], Tuple[bool, Dict[str, str]]]
