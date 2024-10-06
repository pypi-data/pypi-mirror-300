# vim: set fileencoding=utf-8
"""
Application key-value storage.

(c) DevPocket, 2024


Author(s): Michael Bogorad
"""

import sqlalchemy
import sqlalchemy.dialects.sqlite as sqlite_dialect
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from ..errors import DatabaseError
from .models import KeyValue, DomikaKeyValueCreate, DomikaKeyValueRead


async def get(db_session: AsyncSession, user_id: str, key: str) -> KeyValue | None:
    """
    Get value by user id and key.

    Raise:
        errors.DatabaseError: in case when database operation can't be performed.
    """
    try:
        stmt = sqlalchemy.select(KeyValue).where(KeyValue.user_id == user_id).where(KeyValue.key == key)
        return await db_session.scalar(stmt)
    except SQLAlchemyError as e:
        raise DatabaseError(str(e)) from e


async def create_or_update(
    db_session: AsyncSession,
    key_value_in: DomikaKeyValueCreate,
    *,
    commit: bool = True,
) -> KeyValue | None:
    """
    Create or update key_value record.

    Raise:
        errors.DatabaseError: in case when database operation can't be performed.
    """
    stmt = sqlite_dialect.insert(KeyValue)
    stmt = stmt.values(**key_value_in.to_dict())
    stmt = stmt.on_conflict_do_update(
        index_elements=[KeyValue.user_id, KeyValue.key],
        set_={
            "value": stmt.excluded.value,
        },
    )
    stmt = stmt.returning(KeyValue)

    try:
        result = await db_session.scalar(stmt)

        if commit:
            await db_session.commit()
    except SQLAlchemyError as e:
        raise DatabaseError(str(e)) from e

    return result


async def delete(
    db_session: AsyncSession,
    user_id: str,
    key: str,
    *,
    commit: bool = True,
):
    """
    Delete key_value record.

    Raise:
        errors.DatabaseError: in case when database operation can't be performed.
    """
    stmt = sqlalchemy.delete(KeyValue).where(KeyValue.user_id == user_id).where(KeyValue.key == key)

    try:
        await db_session.execute(stmt)

        if commit:
            await db_session.commit()
    except SQLAlchemyError as e:
        raise DatabaseError(str(e)) from e
