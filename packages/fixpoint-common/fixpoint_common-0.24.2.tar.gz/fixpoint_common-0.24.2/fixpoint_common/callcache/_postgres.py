"""A callcache that uses Postgres as a backend"""

__all__ = ["StepPostgresCallCache", "TaskPostgresCallCache"]

from typing import Any, Dict, Optional, Tuple, Type, TypedDict

from psycopg_pool import ConnectionPool, AsyncConnectionPool
from psycopg.rows import dict_row

from fixpoint_common.utils.sql import ParamNameKind, param
from ._shared import (
    CallCache,
    CallCacheKind,
    CacheResult,
    default_json_dumps,
    deserialize_json_val,
)


_TABLE = "fixpoint.callcache"


class StepPostgresCallCache(CallCache):
    """A step callcache that uses Postgres as a backend"""

    cache_kind = CallCacheKind.STEP

    _pg_pool: ConnectionPool
    _apg_pool: Optional[AsyncConnectionPool]

    def __init__(
        self,
        pg_pool: ConnectionPool,
        apg_pool: Optional[AsyncConnectionPool],
    ):
        """
        Args:
            pg_pool: A connection pool to the Postgres database.
        """
        self._pg_pool = pg_pool
        self._apg_pool = apg_pool

    @property
    def _must_apg_pool(self) -> AsyncConnectionPool:
        if self._apg_pool is None:
            raise RuntimeError("No async database connection pool found")
        return self._apg_pool

    def check_cache(
        self,
        *,
        org_id: str,
        run_id: str,
        kind_id: str,
        serialized_args: str,
        type_hint: Optional[Type[Any]] = None,
    ) -> CacheResult[Any]:
        """Check if the result of a task or step call is cached"""
        return _check_cache(
            pg_pool=self._pg_pool,
            org_id=org_id,
            run_id=run_id,
            kind=CallCacheKind.STEP,
            kind_id=kind_id,
            serialized_args=serialized_args,
            type_hint=type_hint,
        )

    def store_result(
        self, *, org_id: str, run_id: str, kind_id: str, serialized_args: str, res: Any
    ) -> None:
        """Store the result of a task or step call"""
        _store_result(
            pg_pool=self._pg_pool,
            org_id=org_id,
            run_id=run_id,
            kind=CallCacheKind.STEP,
            kind_id=kind_id,
            serialized_args=serialized_args,
            res=res,
        )

    async def async_check_cache(
        self,
        *,
        org_id: str,
        run_id: str,
        kind_id: str,
        serialized_args: str,
        type_hint: Optional[Type[Any]] = None,
    ) -> CacheResult[Any]:
        """Check if the result of a task or step call is cached"""
        return await _async_check_cache(
            pg_pool=self._must_apg_pool,
            org_id=org_id,
            run_id=run_id,
            kind=CallCacheKind.STEP,
            kind_id=kind_id,
            serialized_args=serialized_args,
            type_hint=type_hint,
        )

    async def async_store_result(
        self, *, org_id: str, run_id: str, kind_id: str, serialized_args: str, res: Any
    ) -> None:
        """Store the result of a task or step call"""
        await _async_store_result(
            apg_pool=self._must_apg_pool,
            org_id=org_id,
            run_id=run_id,
            kind=CallCacheKind.STEP,
            kind_id=kind_id,
            serialized_args=serialized_args,
            res=res,
        )


class TaskPostgresCallCache(CallCache):
    """A task callcache that uses Postgres as a backend"""

    cache_kind = CallCacheKind.TASK

    _pg_pool: ConnectionPool
    _apg_pool: Optional[AsyncConnectionPool]

    def __init__(
        self,
        pg_pool: ConnectionPool,
        apg_pool: Optional[AsyncConnectionPool],
    ):
        """
        Args:
            pg_pool: A connection pool to the Postgres database.
        """
        self._pg_pool = pg_pool
        self._apg_pool = apg_pool

    @property
    def _must_apg_pool(self) -> AsyncConnectionPool:
        if self._apg_pool is None:
            raise RuntimeError("No async database connection pool found")
        return self._apg_pool

    def check_cache(
        self,
        *,
        org_id: str,
        run_id: str,
        kind_id: str,
        serialized_args: str,
        type_hint: Optional[Type[Any]] = None,
    ) -> CacheResult[Any]:
        """Check if the result of a task or step call is cached"""
        return _check_cache(
            pg_pool=self._pg_pool,
            org_id=org_id,
            run_id=run_id,
            kind=CallCacheKind.TASK,
            kind_id=kind_id,
            serialized_args=serialized_args,
            type_hint=type_hint,
        )

    def store_result(
        self, *, org_id: str, run_id: str, kind_id: str, serialized_args: str, res: Any
    ) -> None:
        """Store the result of a task or step call"""
        _store_result(
            pg_pool=self._pg_pool,
            org_id=org_id,
            run_id=run_id,
            kind=CallCacheKind.TASK,
            kind_id=kind_id,
            serialized_args=serialized_args,
            res=res,
        )

    async def async_check_cache(
        self,
        *,
        org_id: str,
        run_id: str,
        kind_id: str,
        serialized_args: str,
        type_hint: Optional[Type[Any]] = None,
    ) -> CacheResult[Any]:
        """Check if the result of a task or step call is cached"""
        return await _async_check_cache(
            pg_pool=self._must_apg_pool,
            org_id=org_id,
            run_id=run_id,
            kind=CallCacheKind.TASK,
            kind_id=kind_id,
            serialized_args=serialized_args,
            type_hint=type_hint,
        )

    async def async_store_result(
        self, *, org_id: str, run_id: str, kind_id: str, serialized_args: str, res: Any
    ) -> None:
        """Store the result of a task or step call"""
        await _async_store_result(
            apg_pool=self._must_apg_pool,
            org_id=org_id,
            run_id=run_id,
            kind=CallCacheKind.TASK,
            kind_id=kind_id,
            serialized_args=serialized_args,
            res=res,
        )


def _check_cache(
    *,
    pg_pool: ConnectionPool,
    org_id: str,
    run_id: str,
    kind: CallCacheKind,
    kind_id: str,
    serialized_args: str,
    type_hint: Optional[Type[Any]] = None,
) -> CacheResult[Any]:
    with pg_pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            query, params = _new_check_cache_query(
                _TABLE,
                org_id,
                run_id,
                kind,
                kind_id,
                serialized_args,
            )
            cursor.execute(query, params)
            row = cursor.fetchone()
            if not row:
                return CacheResult(found=False, result=None)
            loaded_row = _load_row(row)
            return CacheResult(
                found=True, result=deserialize_json_val(loaded_row["result"], type_hint)
            )


async def _async_check_cache(
    *,
    pg_pool: AsyncConnectionPool,
    org_id: str,
    run_id: str,
    kind: CallCacheKind,
    kind_id: str,
    serialized_args: str,
    type_hint: Optional[Type[Any]] = None,
) -> CacheResult[Any]:
    async with pg_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cursor:
            query, params = _new_check_cache_query(
                _TABLE,
                org_id,
                run_id,
                kind,
                kind_id,
                serialized_args,
            )
            await cursor.execute(query, params)
            row = await cursor.fetchone()
            if not row:
                return CacheResult(found=False, result=None)
            loaded_row = _load_row(row)
            return CacheResult(
                found=True, result=deserialize_json_val(loaded_row["result"], type_hint)
            )


def _new_check_cache_query(
    table: str,
    org_id: str,
    run_id: str,
    kind: CallCacheKind,
    kind_id: str,
    serialized_args: str,
) -> Tuple[str, Dict[str, Any]]:
    def _param(pn: str) -> str:
        return param(ParamNameKind.POSTGRES, pn)

    query = f"""
    SELECT result FROM {table}
    WHERE
        org_id = {_param("org_id")} AND
        run_id = {_param("run_id")} AND
        kind = {_param("kind")} AND
        kind_id = {_param("kind_id")} AND
        serialized_args = {_param("serialized_args")};
    """
    return query, {
        "org_id": org_id,
        "run_id": run_id,
        "kind": kind.value,
        "kind_id": kind_id,
        "serialized_args": serialized_args,
    }


class _Row(TypedDict):
    result: str


def _load_row(row: Any) -> _Row:
    return {
        "result": row["result"],
    }


def _store_result(
    *,
    pg_pool: ConnectionPool,
    org_id: str,
    run_id: str,
    kind: CallCacheKind,
    kind_id: str,
    serialized_args: str,
    res: Any,
) -> None:
    with pg_pool.connection() as conn:
        with conn.cursor() as cursor:
            query, params = _new_store_result_query(
                _TABLE,
                org_id,
                run_id,
                kind,
                kind_id,
                serialized_args,
                res,
            )
            cursor.execute(query, params)
        conn.commit()


async def _async_store_result(
    *,
    apg_pool: AsyncConnectionPool,
    org_id: str,
    run_id: str,
    kind: CallCacheKind,
    kind_id: str,
    serialized_args: str,
    res: Any,
) -> None:
    async with apg_pool.connection() as conn:
        async with conn.cursor() as cursor:
            query, params = _new_store_result_query(
                _TABLE,
                org_id,
                run_id,
                kind,
                kind_id,
                serialized_args,
                res,
            )
            await cursor.execute(query, params)
        await conn.commit()


def _new_store_result_query(
    table: str,
    org_id: str,
    run_id: str,
    kind: CallCacheKind,
    kind_id: str,
    serialized_args: str,
    res: Any,
) -> Tuple[str, Dict[str, Any]]:
    def _param(pn: str) -> str:
        return param(ParamNameKind.POSTGRES, pn)

    query = f"""
    INSERT INTO {table} (org_id, run_id, kind, kind_id, serialized_args, result)
    VALUES (
        {_param("org_id")},
        {_param("run_id")},
        {_param("kind")},
        {_param("kind_id")},
        {_param("serialized_args")},
        {_param("result")}
    );
    """

    return query, {
        "org_id": org_id,
        "run_id": run_id,
        "kind": kind.value,
        "kind_id": kind_id,
        "serialized_args": serialized_args,
        "result": default_json_dumps(res),
    }
