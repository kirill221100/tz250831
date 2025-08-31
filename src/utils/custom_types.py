from collections.abc import Callable, Awaitable
from typing import Annotated, Any
from uuid import uuid4
from sqlalchemy import UUID
from sqlalchemy.orm import mapped_column

uuid_no_pk = Annotated[uuid4, mapped_column(UUID(as_uuid=True), primary_key=False, default=uuid4)]
uuid_pk = Annotated[uuid4, mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)]
AsyncFunc = Callable[..., Awaitable[Any]]
