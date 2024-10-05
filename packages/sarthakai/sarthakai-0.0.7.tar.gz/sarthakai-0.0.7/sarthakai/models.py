from pydantic import BaseModel
from typing import List, Dict, Union
from datetime import datetime


class Chunk(BaseModel):
    text: str
    non_vectorised_addendum_text: str = ""
    embedding: List = None
    page_no: int = 0
    file_source: str = ""
    article_id: str = ""
    metadata: Dict[str, Union[str, datetime]] = None

    @property
    def fields_in_chromadb_metadata_format(self):
        metadata = self.metadata or {}
        if self.non_vectorised_addendum_text:
            metadata["non_vectorised_addendum_text"] = self.non_vectorised_addendum_text
        if self.page_no:
            metadata["page_no"] = self.page_no
        if self.file_source:
            metadata["file_source"] = self.file_source
        metadata = metadata or None
        return metadata


class VectorSearchResponse(BaseModel):
    document: str
    distance: float
    metadata: Union[Dict[str, str], None] = None


class WebSearchResponse(BaseModel):
    url: str
    title: str = ""
    snippet: str = ""
