from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass(frozen=True, kw_only=True)
class Auth:
    """Dataclass for storing auth details specific to an implementation
    (e.g., depending which identity provider you use, how you do authorization,
    etc). We include some fields that we believe are generic to simplify
    implementations such as the `user_id`.

    The Auth object is provided by the TokenVerifier and passed on the Context
    on every request.
    """
    user_id: Optional[str] = None
    properties: dict[str, Any] = field(default_factory=dict)
