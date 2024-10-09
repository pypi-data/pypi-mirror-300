from nuclia_models.common.client import ClientType
from nuclia_models.common.pagination import Pagination
from nuclia_models.common.user import UserType
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import field_validator
from pydantic.main import create_model
from typing import Generic
from typing import TypeVar

import re

T = TypeVar("T")


class BaseConfigModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class GenericFilter(BaseConfigModel, Generic[T]):
    eq: T | None = None
    gt: T | None = None
    ge: T | None = None
    lt: T | None = None
    le: T | None = None
    ne: T | None = None
    isnull: bool | None = None


class StringFilter(GenericFilter[str]):
    like: str | None = None
    ilike: str | None = None


class AuditMetadata(StringFilter):
    key: str


class QueryFiltersCommon(BaseConfigModel):
    id: BaseConfigModel | None = Field(None)
    date: BaseConfigModel | None = Field(None, serialization_alias="event_date")
    user_id: GenericFilter[str] | None = None
    user_type: GenericFilter[UserType] | None = None
    client_type: GenericFilter[ClientType] | None = None
    total_duration: GenericFilter[float] | None = None
    audit_metadata: list[AuditMetadata] | None = Field(
        None, serialization_alias="data.user_request.audit_metadata"
    )


class QueryFiltersSearch(QueryFiltersCommon):
    question: StringFilter | None = Field(None, serialization_alias="data.request.body")
    resources_count: StringFilter | None = Field(
        None,
        serialization_alias="data.resources_count",
    )
    filter: BaseConfigModel | None = Field(None, serialization_alias="data.request.filter")
    learning_id: BaseConfigModel | None = Field(None, serialization_alias="data.request.learning_id")


class QueryFiltersChat(QueryFiltersSearch):
    rephrased_question: StringFilter | None = Field(
        None, serialization_alias="data.request.rephrased_question"
    )
    answer: StringFilter | None = Field(None, serialization_alias="data.request.answer")
    retrieved_context: BaseConfigModel | None = Field(None, serialization_alias="data.request.context")
    chat_history: BaseConfigModel | None = Field(None, serialization_alias="data.request.chat_context")
    feedback_good: StringFilter | None = Field(None, serialization_alias="data.feedback.good")
    feedback_comment: StringFilter | None = Field(None, serialization_alias="data.feedback.feedback")
    model: StringFilter | None = Field(None, serialization_alias="data.model")
    rag_strategies_names: BaseConfigModel | None = Field(None, serialization_alias="data.rag_strategies")
    rag_strategies: BaseConfigModel | None = Field(
        None, serialization_alias="data.user_request.rag_strategies"
    )
    status: StringFilter | None = Field(None, serialization_alias="data.request.status")
    time_to_first_char: BaseConfigModel | None = Field(
        None, serialization_alias="data.generative_answer_first_chunk_time"
    )


def create_dynamic_model(name: str, base_model: QueryFiltersChat):
    field_definitions = {}
    field_type_map = {
        "id": int,
        "user_type": UserType | None,
        "client_type": ClientType | None,
        "total_duration": float | None,
        "time_to_first_char": float | None,
    }
    for field_name in base_model.model_fields.keys():
        field_type = field_type_map.get(field_name, str | None)

        field_definitions[field_name] = (field_type, Field(default=None))

    return create_model(name, **field_definitions)


ActivityLogsQueryResponse = create_dynamic_model(
    name="ActivityLogsQueryResponse", base_model=QueryFiltersChat
)


class ActivityLogsQueryCommon(BaseConfigModel):
    year_month: str

    @field_validator("year_month")
    def validate_year_month(cls, value):
        if not re.match(r"^\d{4}-(0[1-9]|1[0-2])$", value):
            raise ValueError("year_month must be in the format YYYY-MM")
        return value

    @staticmethod
    def _validate_show(show: set[str], model: type[QueryFiltersCommon]):
        allowed_fields = list(model.__annotations__.keys())
        for field in show:
            if field.startswith("audit_metadata."):
                continue
            if field not in allowed_fields:
                raise ValueError(f"{field} is not a field. List of fields: {allowed_fields}")
        return show


class ActivityLogsQuery(ActivityLogsQueryCommon):
    show: set[str] = set()
    filters: QueryFiltersCommon

    @field_validator("show")
    def validate_show(cls, show: set[str]):
        return cls._validate_show(show=show, model=QueryFiltersCommon)


class ActivityLogsChatQuery(ActivityLogsQueryCommon):
    show: set[str] = set()
    filters: QueryFiltersChat

    @field_validator("show")
    def validate_show(cls, show: set[str]):
        return cls._validate_show(show=show, model=QueryFiltersChat)


class ActivityLogsSearchQuery(ActivityLogsQueryCommon):
    show: set[str] = set()
    filters: QueryFiltersSearch

    @field_validator("show")
    def validate_show(cls, show: set[str]):
        return cls._validate_show(show=show, model=QueryFiltersSearch)


class ActivityLogsSearchQueryPagination(ActivityLogsSearchQuery):
    pagination: Pagination


class ActivityLogsChatQueryPagination(ActivityLogsChatQuery):
    pagination: Pagination


class ActivityLogsQueryPagination(ActivityLogsQuery):
    pagination: Pagination
