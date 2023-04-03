from models.models import (
    Document,
    DocumentMetadataFilter,
    Query,
    QueryResult,
)
from pydantic import BaseModel
from typing import List, Optional


class IndexRequest(BaseModel):
    name: str


class UpsertRequest(BaseModel):
    index = IndexRequest
    documents: List[Document]


class UpsertResponse(BaseModel):
    index = IndexRequest
    ids: List[str]


class QueryRequest(BaseModel):
    index = IndexRequest
    queries: List[Query]


class QueryResponse(BaseModel):
    results: List[QueryResult]


class DeleteRequest(BaseModel):
    index = IndexRequest
    ids: Optional[List[str]] = None
    filter: Optional[DocumentMetadataFilter] = None
    delete_all: Optional[bool] = False


class DeleteResponse(BaseModel):
    success: bool
