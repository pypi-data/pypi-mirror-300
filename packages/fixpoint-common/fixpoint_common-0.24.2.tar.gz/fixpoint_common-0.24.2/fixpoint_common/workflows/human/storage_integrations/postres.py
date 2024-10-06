"""On-disk document storage for workflows"""

__all__ = ["PostgresHumanTaskStorage"]

from typing import Any, Dict, List, Optional

from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool, AsyncConnectionPool

from fixpoint_common.constants import NULL_COL_ID
from fixpoint_common.types import HumanTaskEntry, ListHumanTaskEntriesRequest
from fixpoint_common._storage import definitions as storage_definitions
from fixpoint_common.utils.sql import ParamNameKind
from fixpoint_common.workflows.human._human_task_storage import HumanTaskStorage
from fixpoint_common.workflows.human.storage_integrations.shared import (
    get_query,
    create_query,
    update_query,
    list_query,
)


class PostgresHumanTaskStorage(HumanTaskStorage):
    """On-disk document storage for workflows"""

    _pool: ConnectionPool
    _apool: Optional[AsyncConnectionPool]
    _table: str = "fixpoint.task_entries"

    def __init__(self, pool: ConnectionPool, apool: Optional[AsyncConnectionPool]):
        self._pool = pool
        self._apool = apool
        with self._pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(storage_definitions.HUMAN_TASKS_POSTGRES_TABLE)
            conn.commit()

    @property
    def _must_apool(self) -> AsyncConnectionPool:
        if self._apool is None:
            raise RuntimeError("no async database pool")
        return self._apool

    def get(
        self,
        org_id: str,
        id: str,  # pylint: disable=redefined-builtin
        workflow_id: Optional[str] = None,
        workflow_run_id: Optional[str] = None,
    ) -> Optional[HumanTaskEntry]:
        query, params = get_query(
            ParamNameKind.POSTGRES,
            self._table,
            org_id,
            id,
            workflow_id,
            workflow_run_id,
        )
        with self._pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as dbcursor:
                dbcursor.execute(query, params)
                row = dbcursor.fetchone()
                return self._load_row(row) if row else None

    async def async_get(
        self,
        org_id: str,
        id: str,  # pylint: disable=redefined-builtin
        workflow_id: Optional[str] = None,
        workflow_run_id: Optional[str] = None,
    ) -> Optional[HumanTaskEntry]:
        query, params = get_query(
            ParamNameKind.POSTGRES,
            self._table,
            org_id,
            id,
            workflow_id,
            workflow_run_id,
        )
        async with self._must_apool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as dbcursor:
                await dbcursor.execute(query, params)
                row = await dbcursor.fetchone()
                return self._load_row(row) if row else None

    def create(self, org_id: str, task: HumanTaskEntry) -> None:
        query, params = create_query(ParamNameKind.POSTGRES, self._table, org_id, task)
        with self._pool.connection() as conn:
            with conn.cursor() as dbcursor:
                dbcursor.execute(query, params)
                conn.commit()

    async def async_create(self, org_id: str, task: HumanTaskEntry) -> None:
        query, params = create_query(ParamNameKind.POSTGRES, self._table, org_id, task)
        async with self._must_apool.connection() as conn:
            async with conn.cursor() as dbcursor:
                await dbcursor.execute(query, params)
                await conn.commit()

    def update(self, org_id: str, task: HumanTaskEntry) -> None:
        query, params = update_query(ParamNameKind.POSTGRES, self._table, org_id, task)
        with self._pool.connection() as conn:
            with conn.cursor() as dbcursor:
                dbcursor.execute(query, params)
                conn.commit()

    async def async_update(self, org_id: str, task: HumanTaskEntry) -> None:
        query, params = update_query(ParamNameKind.POSTGRES, self._table, org_id, task)
        async with self._must_apool.connection() as conn:
            async with conn.cursor() as dbcursor:
                await dbcursor.execute(query, params)
                await conn.commit()

    def list(
        self,
        org_id: str,
        req: ListHumanTaskEntriesRequest,
    ) -> List[HumanTaskEntry]:
        """Get a list of tasks from PostgreSQL."""
        query, params = list_query(
            ParamNameKind.POSTGRES,
            self._table,
            org_id,
            req,
        )

        with self._pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as dbcursor:
                dbcursor.execute(query, params)
                rows = dbcursor.fetchall()

                return [self._load_row(row) for row in rows]

    async def async_list(
        self,
        org_id: str,
        req: ListHumanTaskEntriesRequest,
    ) -> List[HumanTaskEntry]:
        """Get a list of tasks from PostgreSQL."""
        query, params = list_query(
            ParamNameKind.POSTGRES,
            self._table,
            org_id,
            req,
        )

        async with self._must_apool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as dbcursor:
                await dbcursor.execute(query, params)
                rows = await dbcursor.fetchall()

                return [self._load_row(row) for row in rows]

    def _load_row(self, row: Any) -> HumanTaskEntry:
        wid = row["workflow_id"]
        if wid == NULL_COL_ID:
            wid = None
        wrid = row["workflow_run_id"]
        if wrid == NULL_COL_ID:
            wrid = None

        return HumanTaskEntry(
            id=row["id"],
            workflow_id=wid,
            workflow_run_id=wrid,
            task_id=row["task_id"],
            source_node=row["source_node"],
            status=row["status"],
            entry_fields=row["entry_fields"],
            metadata=row["metadata"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )
