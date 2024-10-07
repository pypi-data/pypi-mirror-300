"""
@autoapi False
"""
from typing import Union

from rhino_health.lib.endpoints.endpoint import Endpoint
from rhino_health.lib.endpoints.semantic_map.semantic_map_dataclass import (
    SemanticMapApproveList,
    SemanticMapDataclass,
    SemanticMapInput,
    Vocabulary,
    VocabularyInput,
    VocabularySearch,
)
from rhino_health.lib.utils import rhino_error_wrapper

BUFFER_TIME_IN_SEC = 300


class SemanticMapEndpoints(Endpoint):
    """
    @autoapi False

    Endpoints to interact with semantic maps
    """

    @property
    def semantic_map_dataclass(self):
        """
        @autoapi False
        :return:
        """
        return SemanticMapDataclass

    @rhino_error_wrapper
    def vocabulary_search(self, vocabulary_search_params: VocabularySearch):
        return self.session.post(
            f"/vocabulary_search/",
            vocabulary_search_params.dict(by_alias=True),
            adapter_kwargs={"data_as_json": True},
        )

    @rhino_error_wrapper
    def create_semantic_map(self, semantic_map_input: SemanticMapInput):
        data = semantic_map_input.dict(by_alias=True)
        result = self.session.post(
            "/semantic_mappings",
            data=data,
            adapter_kwargs={"data_as_json": True},
        )
        return result.to_dataclass(self.semantic_map_dataclass)

    @rhino_error_wrapper
    def get_semantic_map(self, semantic_map_or_uid: Union[str, SemanticMapDataclass]):
        result = self.session.get(
            f"/semantic_mappings/{semantic_map_or_uid if isinstance(semantic_map_or_uid, str) else semantic_map_or_uid.uid}"
        )
        return result.to_dataclass(self.semantic_map_dataclass)

    @rhino_error_wrapper
    def get_semantic_map_data(self, semantic_map_or_uid: Union[str, SemanticMapDataclass]):
        result = self.session.get(
            f"/semantic_mappings/{semantic_map_or_uid if isinstance(semantic_map_or_uid, str) else semantic_map_or_uid.uid}/data"
        )
        return result  # TODO: Convert to dataclass.

    @rhino_error_wrapper
    def approve_mappings(self, semantic_map_uid: str, mapping_data: SemanticMapApproveList):
        data = mapping_data.dict(by_alias=True)
        result = self.session.post(
            f"/semantic_mappings/{semantic_map_uid}/approve_mappings",
            data=data,
            adapter_kwargs={"data_as_json": True},
        )
        return result  # TODO: Convert to dataclass

    def create_vocabulary(self, vocabulary_input: VocabularyInput):
        data = vocabulary_input.dict(by_alias=True)
        result = self.session.post(
            "/custom_vocabularies/",
            data=data,
            adapter_kwargs={"data_as_json": True},
        )
        return result.to_dataclass(Vocabulary)

    def get_vocabulary(self, vocabulary_or_uid: Union[str, Vocabulary]):
        result = self.session.get(
            f"/custom_vocabularies/{vocabulary_or_uid if isinstance(vocabulary_or_uid, str) else vocabulary_or_uid.uid}",
        )
        return result.to_dataclass(Vocabulary)
