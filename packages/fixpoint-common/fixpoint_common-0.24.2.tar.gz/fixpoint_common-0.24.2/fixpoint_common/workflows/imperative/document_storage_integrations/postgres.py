"""On-disk document storage for workflows"""

from typing import Any, List, Optional

from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

from fixpoint_common.constants import NULL_COL_ID
from fixpoint_common.types import Document
from fixpoint_common.utils.sql import ParamNameKind
from fixpoint_common.errors import NotFoundError
from fixpoint_common.workflows.imperative._doc_storage import DocStorage
from .shared import (
    get_document_query,
    create_document_query,
    update_document_query,
    list_documents_query,
)


class PostgresDocStorage(DocStorage):
    """On-disk document storage for workflows"""

    _pool: ConnectionPool
    _table: str = "fixpoint.documents"

    def __init__(self, pool: ConnectionPool):
        self._pool = pool

    def get(
        self,
        org_id: str,
        id: str,  # pylint: disable=redefined-builtin
        workflow_id: Optional[str] = None,
        workflow_run_id: Optional[str] = None,
    ) -> Optional[Document]:
        with self._pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as dbcursor:
                query, params = get_document_query(
                    ParamNameKind.POSTGRES,
                    self._table,
                    org_id,
                    id,
                    workflow_id,
                    workflow_run_id,
                )
                dbcursor.execute(query, params)
                row = dbcursor.fetchone()

                if not row:
                    return None

                return self._load_row(row)

    def create(self, org_id: str, document: Document) -> None:
        with self._pool.connection() as conn:
            with conn.cursor() as dbcursor:
                query, params = create_document_query(
                    ParamNameKind.POSTGRES,
                    self._table,
                    org_id,
                    document,
                )
                dbcursor.execute(query, params)
                conn.commit()

    def update(self, org_id: str, document: Document) -> None:
        with self._pool.connection() as conn:
            with conn.cursor() as dbcursor:
                query, params = update_document_query(
                    ParamNameKind.POSTGRES,
                    self._table,
                    org_id,
                    document,
                )
                dbcursor.execute(query, params)
                if dbcursor.rowcount == 0:
                    raise NotFoundError("Document not found")
                conn.commit()

    def list(
        self,
        org_id: str,
        path: Optional[str] = None,
        workflow_id: Optional[str] = None,
        workflow_run_id: Optional[str] = None,
        task: Optional[str] = None,
        step: Optional[str] = None,
    ) -> List[Document]:
        with self._pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as dbcursor:
                query, params = list_documents_query(
                    ParamNameKind.POSTGRES,
                    self._table,
                    org_id,
                    path=path,
                    workflow_id=workflow_id,
                    workflow_run_id=workflow_run_id,
                    task=task,
                    step=step,
                )
                dbcursor.execute(query, params)
                rows = dbcursor.fetchall()
                return [self._load_row(row) for row in rows]

    def _load_row(self, row: Any) -> Document:
        wid = row["workflow_id"]
        if wid == NULL_COL_ID:
            wid = None
        wrid = row["workflow_run_id"]
        if wrid == NULL_COL_ID:
            wrid = None
        return Document(
            id=row["id"],
            workflow_id=wid,
            workflow_run_id=wrid,
            path=row["path"],
            metadata=row["metadata"],
            contents=row["contents"],
            versions=row["versions"],
            media_type=row["media_type"],
        )
