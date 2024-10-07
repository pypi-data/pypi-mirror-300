"""
@autoapi False

INTERNAL USE ONLY!
"""
from enum import Enum
from typing import Any, Callable, Dict, List, Literal, Optional

from pydantic import BaseModel, Field
from typing_extensions import Annotated

from rhino_health.lib.dataclass import RhinoBaseModel, UIDField
from rhino_health.lib.endpoints.project.project_baseclass import WithinProjectModel
from rhino_health.lib.endpoints.user.user_baseclass import UserCreatedModel
from rhino_health.lib.endpoints.workgroup.workgroup_baseclass import (
    PrimaryWorkgroupModel,
    WithinWorkgroupModel,
)
from rhino_health.lib.metrics.base_metric import BaseMetric


class Subcategories(BaseModel):
    """
    A class to represent the subcategories of a vocabulary
    We allow the user to specify a list of subcategories to filter on, and allow control over whether the items in
    the list are "or"ed or "and"ed together. If both lists are supplied, both lists are applied with an "and" between them.
    """

    or_list: List[str] = None  # The items in the list are "or"ed together
    and_list: List[str] = None  # The items in the list are "and"ed together


class VocabularyTerm(BaseModel):
    term_display_name: str
    term_identifier: str
    subcategories: Optional[list]
    term_class: Optional[str]
    source_vocabulary_name: Optional[str]
    score: Optional[float] = 0


class VocabularyInput(BaseModel):
    name: str
    prefiltering_service_table: str
    description: str
    primary_workgroup: str
    base_version_uid: Optional[str] = None
    version: Optional[int] = 0
    type: Literal["Standard", "Custom"]
    terms: Optional[List[VocabularyTerm]] = None
    creator: str
    possible_domain_names: Optional[List[str]] = None


class Vocabulary(VocabularyInput):
    uid: str


class VocabularyFilters(BaseModel):
    subcategories: Optional[Subcategories] = None
    term_class: Optional[str] = None

    @staticmethod
    def from_dict(filters_dict):
        vocabulary_filters = VocabularyFilters()
        if filters_dict:
            if "sub_categories" in filters_dict:
                vocabulary_filters.sub_categories = Subcategories(**filters_dict["sub_categories"])
            if "term_class" in filters_dict:
                vocabulary_filters.term_class = filters_dict["term_class"]
            return vocabulary_filters


class SearchMode(str, Enum):
    """
    A class to represent the search mode for the vocabulary search
    The search mode determines the query that is used to search the OpenSearch DB.
    The possible values are:
    - closest: The search term is matched against the term_display_name using the custom ngram predefined in
    the index (which is a table in the DB) creation. See more details about ngram here https://opensearch.org/docs/latest/analyzers/tokenizers/index/.
    - contains_display_name: The search term is matched against the term_display_name, and matches values that starts with or contains the search term.
    - contains_identifier: The search term is matched against the term_identifier, and matches values that starts with or contains the search term.
    """

    CLOSEST = "closest"
    CONTAINS_DISPLAY_NAME = "contains_display_name"
    CONTAINS_IDENTIFIER = "contains_identifier"


class VocabularySearch(RhinoBaseModel):
    display_name: str
    filter_options: Optional[List[VocabularyFilters]] = None
    num_results: Optional[int] = 100
    search_mode: Optional[SearchMode] = SearchMode.CLOSEST


class DatasetColumn(BaseModel):
    dataset_uid: str
    field_name: str


class SemanticMapInput(RhinoBaseModel):
    name: str
    description: Optional[str] = ""
    primary_workgroup_uid: Annotated[str, Field(alias="primary_workgroup")]
    base_version_uid: Optional[str] = None
    version: Optional[int] = 0
    input_vocabulary_uid: Annotated[str, Field(alias="input_vocabulary")]
    output_vocabulary_uid: Annotated[str, Field(alias="output_vocabulary")]
    output_vocabulary_filters: Optional[List[VocabularyFilters]] = None
    project_uid: Annotated[str, Field(alias="project")]
    source_dataset_columns: List[DatasetColumn]


class SemanticMapProcessingStatus(str, Enum):
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    NEEDS_REVIEW = "Needs Review"
    APPROVED = "Approved"
    ERROR = "Error"


class SemanticMapDataclass(
    PrimaryWorkgroupModel, WithinProjectModel, UserCreatedModel, SemanticMapInput
):
    processing_status: SemanticMapProcessingStatus
    processing_error_message: Optional[List[str]] = []
    input_vocabulary_uid: Annotated[Any, Field(alias="input_vocabulary")]
    output_vocabulary_uid: Annotated[Any, Field(alias="output_vocabulary")]
    # input_vocabulary_uid: Annotated[Vocabulary, UIDField(alias="input_vocabulary")]
    # output_vocabulary_uid: Annotated[Vocabulary, UIDField(alias="output_vocabulary")]
    uid: str

    def wait_for_completion(
        self,
        timeout_seconds: int = 6000,
        poll_frequency: int = 10,
        print_progress: bool = True,
    ):
        from rhino_health.lib.endpoints.semantic_map.semantic_map_endpoints import (
            SemanticMapEndpoints,
        )

        semantic_map_endpoints = SemanticMapEndpoints(self.session)
        return self._wait_for_completion(
            name="semantic map processing",
            is_complete=self._finished_processing,
            query_function=lambda semantic_map: semantic_map_endpoints.get_semantic_map(self.uid),
            validation_function=lambda old, new: (new._finished_processing),
            timeout_seconds=timeout_seconds,
            poll_frequency=poll_frequency,
            print_progress=print_progress,
        )

    @property
    def _finished_processing(self):
        return self.processing_status not in {
            SemanticMapProcessingStatus.NOT_STARTED,
            SemanticMapProcessingStatus.IN_PROGRESS,
        }


class SemanticMapApproveEntry(BaseModel):
    source_term_name: str
    target_term_name: str
    target_identifier: str
    is_approved: bool


class SemanticMapApproveList(RhinoBaseModel):
    entries: List[SemanticMapApproveEntry]


class SemanticMapEntry(BaseModel):
    entry_uid: str
    source_term_name: str
    target_term_name: str
    recommendation_data: List[Dict[str, Any]]
    num_appearances: int
    created_at: str
    status: Literal["calculating", "failed", "needs_review", "approved"]
    is_approved: bool
    approved_at: str
    approved_by: Dict[str, str]
    index: int
