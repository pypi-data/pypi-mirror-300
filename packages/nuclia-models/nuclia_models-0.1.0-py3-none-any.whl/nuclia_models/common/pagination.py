from pydantic import BaseModel
from pydantic import Field
from typing import Annotated
from typing import Optional


class Pagination(BaseModel):
    limit: Annotated[int, Field(ge=0, le=1000)] = 10
    starting_after: Optional[int] = None
    ending_before: Optional[int] = None
