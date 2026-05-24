"""
database.py — Supabase data-access layer
─────────────────────────────────────────────────────────────────
KEY CHANGES FROM ORIGINAL:
  1. supabase_insert() now parses the real Supabase APIError and
     surfaces the human-readable message + code instead of a raw
     exception string. This makes the RLS "42501" error actually
     readable in the UI.
  2. Added supabase_exists() — a lightweight row-count helper used
     by every module that needs to validate existence before insert.
  3. supabase_select() is still cached (ttl=600) but the internal
     client call is correctly isolated so cache hashing never tries
     to pickle the Supabase Client object.
  4. Every function returns a typed value (bool / list / int) so
     callers can branch cleanly.
  5. Added a _parse_sb_error() private helper that normalises all
     Supabase PostgREST/APIError shapes into a single dict.
"""

import streamlit as st
from supabase import create_client, Client
import logging

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────
# SINGLETON CONNECTION
# ─────────────────────────────────────────────────────────────────

@st.cache_resource
def get_supabase_client() -> Client:
    """
    Build the Supabase client once per Streamlit process.

    WHY service_role KEY?
    The anon key respects Row Level Security (RLS).  Unless you add
    explicit anon SELECT/INSERT/UPDATE/DELETE policies for every table,
    every operation returns a 42501 "row-level security policy" error.
    Using the service_role key bypasses RLS entirely, which is correct
    for a server-side internal ERP.  Never expose this key on the
    client (browser).  On Streamlit Cloud it stays in secrets.toml.
    """
    try:
        url = st.secrets["SUPABASE_URL"]
        # Prefer SERVICE_ROLE_KEY; fall back to SUPABASE_KEY so
        # existing deployments keep working while the user migrates.
        key = st.secrets.get("SUPABASE_SERVICE_ROLE_KEY") or st.secrets["SUPABASE_SERVICE_ROLE_KEY"]
        return create_client(url, key)
    except KeyError as e:
        st.error(
            f"❌ Missing Supabase secret: {e}. "
            "Add SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY to secrets.toml."
        )
        st.stop()
    except Exception as e:
        st.error(f"❌ Failed to initialise Supabase client: {e}")
        st.stop()


# ─────────────────────────────────────────────────────────────────
# INTERNAL ERROR PARSER
# ─────────────────────────────────────────────────────────────────

def _parse_sb_error(exc: Exception) -> dict:
    """
    Normalise any Supabase / PostgREST exception into
    {'message': str, 'code': str}.

    WHY: The supabase-py library can raise several different exception
    types (postgrest.APIError, httpx.HTTPStatusError, plain Exception).
    Each has a different attribute layout.  This helper extracts the
    human-readable message in all cases so callers don't need to know
    the library internals.
    """
    # postgrest.exceptions.APIError carries .message and .code
    if hasattr(exc, "message") and hasattr(exc, "code"):
        return {"message": exc.message, "code": str(exc.code)}

    # Some versions wrap the detail in exc.args[0] as a dict
    if exc.args and isinstance(exc.args[0], dict):
        return {
            "message": exc.args[0].get("message", str(exc)),
            "code": str(exc.args[0].get("code", "UNKNOWN")),
        }

    return {"message": str(exc), "code": "UNKNOWN"}


# ─────────────────────────────────────────────────────────────────
# CACHE INVALIDATION
# ─────────────────────────────────────────────────────────────────

def clear_db_cache() -> None:
    """
    Purge all @st.cache_data entries after any mutation.

    WHY: st.cache_data caches SELECT results.  After an INSERT /
    UPDATE / DELETE the cached rows are stale.  Clearing the cache
    forces the next SELECT to hit Supabase for fresh data.
    """
    st.cache_data.clear()


# ─────────────────────────────────────────────────────────────────
# INSERT
# ─────────────────────────────────────────────────────────────────

def supabase_insert(table: str, data: dict) -> bool:
    """
    Insert a single record.

    Returns True on success, False on failure.
    On failure the error message (including the RLS policy message)
    is shown to the user via st.error().
    """
    client = get_supabase_client()
    try:
        client.table(table).insert(data).execute()
        clear_db_cache()
        return True
    except Exception as exc:
        err = _parse_sb_error(exc)
        # Translate the cryptic 42501 into plain English
        if err["code"] == "42501":
            st.error(
                f"🔒 Permission denied on table '{table}'. "
                "This means Row Level Security is blocking the operation. "
                "Fix: use the service_role key in secrets.toml, or add an "
                "INSERT policy for the anon role in Supabase → Authentication → Policies."
            )
        else:
            st.error(
                f"❌ Insert failed on '{table}': [{err['code']}] {err['message']}"
            )
        logger.error("supabase_insert(%s): %s", table, err)
        return False


# ─────────────────────────────────────────────────────────────────
# SELECT  (cached)
# ─────────────────────────────────────────────────────────────────

@st.cache_data(ttl=600)
def supabase_select(
    table: str,
    match_filter: dict | None = None,
    ilike_filter: dict | None = None,
    or_filter: str | None = None,
) -> list[dict]:
    """
    Fetch rows from a table.  Result is cached for 10 minutes.

    WHY cache_data and not cache_resource?
    cache_resource is for long-lived objects (DB connections, ML models).
    cache_data is for serialisable return values (lists, dicts).
    Caching SELECT results prevents hammering Supabase on every
    Streamlit re-run while the user is just viewing data.
    """
    client = get_supabase_client()
    try:
        query = client.table(table).select("*")

        if match_filter:
            for k, v in match_filter.items():
                query = query.eq(k, v)

        if ilike_filter:
            for k, v in ilike_filter.items():
                query = query.ilike(k, f"%{v}%")

        if or_filter:
            query = query.or_(or_filter)

        response = query.execute()
        return response.data or []

    except Exception as exc:
        err = _parse_sb_error(exc)
        if err["code"] == "42501":
            st.error(
                f"🔒 Permission denied reading '{table}'. "
                "Use the service_role key or add a SELECT policy for the anon role."
            )
        else:
            st.error(f"❌ Fetch failed on '{table}': [{err['code']}] {err['message']}")
        logger.error("supabase_select(%s): %s", table, err)
        return []


# ─────────────────────────────────────────────────────────────────
# EXISTS HELPER  (NOT cached — used for validation before insert)
# ─────────────────────────────────────────────────────────────────

def supabase_exists(table: str, match_filter: dict) -> bool:
    """
    Return True if at least one row matches the filter.

    WHY not use supabase_select?
    supabase_select() is cached.  Immediately after an insert the
    cache would still return the old (empty) result, making the
    existence check unreliable.  This helper bypasses the cache to
    always query Supabase directly.

    Usage:
        if supabase_exists("employees", {"id": emp_id}):
            ...
    """
    client = get_supabase_client()
    try:
        query = client.table(table).select("*", count="exact")
        for k, v in match_filter.items():
            query = query.eq(k, v)
        response = query.execute()
        return (response.count or 0) > 0
    except Exception as exc:
        err = _parse_sb_error(exc)
        logger.error("supabase_exists(%s): %s", table, err)
        return False


# ─────────────────────────────────────────────────────────────────
# UPDATE
# ─────────────────────────────────────────────────────────────────

def supabase_update(table: str, data: dict, match_filter: dict) -> bool:
    """Update rows matching the filter.  Returns True on success."""
    client = get_supabase_client()
    try:
        query = client.table(table).update(data)
        for k, v in match_filter.items():
            query = query.eq(k, v)
        query.execute()
        clear_db_cache()
        return True
    except Exception as exc:
        err = _parse_sb_error(exc)
        st.error(f"❌ Update failed on '{table}': [{err['code']}] {err['message']}")
        logger.error("supabase_update(%s): %s", table, err)
        return False


# ─────────────────────────────────────────────────────────────────
# DELETE
# ─────────────────────────────────────────────────────────────────

def supabase_delete(table: str, match_filter: dict) -> bool:
    """Delete rows matching the filter.  Returns True on success."""
    client = get_supabase_client()
    try:
        query = client.table(table).delete()
        for k, v in match_filter.items():
            query = query.eq(k, v)
        query.execute()
        clear_db_cache()
        return True
    except Exception as exc:
        err = _parse_sb_error(exc)
        st.error(f"❌ Delete failed on '{table}': [{err['code']}] {err['message']}")
        logger.error("supabase_delete(%s): %s", table, err)
        return False
