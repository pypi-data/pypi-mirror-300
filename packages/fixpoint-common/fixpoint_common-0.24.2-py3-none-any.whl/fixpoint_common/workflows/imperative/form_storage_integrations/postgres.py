"""On-disk document storage for workflows"""

import json
from typing import Any, List, Optional

from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool
from pydantic import BaseModel

from fixpoint_common.types import Form
from fixpoint_common.utils.sql import ParamNameKind
from fixpoint_common.workflows.imperative._form_storage import FormStorage
from .shared import (
    new_get_form_query,
    new_create_form_query,
    new_update_form_query,
    new_list_forms_query,
)


class PostgresFormStorage(FormStorage):
    """Postgres form storage for workflows"""

    _pool: ConnectionPool

    def __init__(self, pool: ConnectionPool):
        self._pool = pool

    def get(
        self, org_id: str, id: str  # pylint: disable=redefined-builtin
    ) -> Optional[Form[BaseModel]]:
        """Get the given Form"""
        with self._pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as dbcursor:
                query, args = new_get_form_query(
                    ParamNameKind.POSTGRES,
                    "fixpoint.forms_with_metadata",
                    org_id,
                    id,
                )
                dbcursor.execute(query, args)
                row = dbcursor.fetchone()
                if not row:
                    return None
                return self._load_row(row)

    def create(self, org_id: str, form: Form[BaseModel]) -> None:
        """Create a new Form"""
        with self._pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as dbcursor:
                query, params = new_create_form_query(
                    ParamNameKind.POSTGRES,
                    "fixpoint.forms_with_metadata",
                    org_id,
                    form,
                )
                dbcursor.execute(query, params)
            conn.commit()

    def update(self, org_id: str, form: Form[BaseModel]) -> None:
        """Update an existing Form"""
        with self._pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as dbcursor:
                query, params = new_update_form_query(
                    ParamNameKind.POSTGRES,
                    "fixpoint.forms_with_metadata",
                    org_id,
                    form,
                )
                dbcursor.execute(query, params)
            conn.commit()

    def list(
        self,
        org_id: str,
        path: Optional[str] = None,
        workflow_run_id: Optional[str] = None,
    ) -> List[Form[BaseModel]]:
        """List all Forms

        If path is provided, list Forms in the given path.
        """
        with self._pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as dbcursor:
                query, params = new_list_forms_query(
                    ParamNameKind.POSTGRES,
                    "fixpoint.forms_with_metadata",
                    org_id,
                    path,
                    workflow_run_id,
                )
                dbcursor.execute(query, params)
                return [self._load_row(row) for row in dbcursor]

    def _load_row(self, row: Any) -> Form[BaseModel]:
        return Form.deserialize(
            {
                "id": row["id"],
                "workflow_id": row["workflow_id"],
                "workflow_run_id": row["workflow_run_id"],
                "metadata": row["metadata"],
                "path": row["path"],
                "contents": row["contents"],
                "form_schema": json.loads(row["form_schema"]),
                "versions": row["versions"],
                "task": row["task"],
                "step": row["step"],
            }
        )
