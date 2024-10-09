from typing import Optional, Sequence, Tuple

from pydantic import BaseModel

from _typeshed import Incomplete

logger: Incomplete

def camel_case(s: str) -> str: ...

class UrlModel(BaseModel):
    pattern_name: str
    namespace: str
    url_parts: Tuple[str, ...]
    js_vars: Tuple[str, ...]
    url_lookup: str
    is_alternative: bool
    def matches(self, name: str, params: Optional[Tuple[str]] = ...) -> bool: ...
    @property
    def js_func_name(self): ...
    @property
    def url(self): ...
    @property
    def js_literal(self): ...
    @property
    def as_function(self): ...
    @property
    def as_class_prop(self): ...
    @property
    def as_arrow_func(self): ...
    @property
    def as_arrow_func_property(self): ...

class UrlModels(BaseModel):
    urls: Sequence[UrlModel]
    def filtered_by_name(self, match=...): ...
    @classmethod
    def all_urls(cls): ...

def all_urls(): ...
