import streamlit as st
from supabase import create_client, Client
import logging

# ─────────────────────────────────────────────────────────────────
# SINGLETON DATABASE CONNECTION (SUPABASE)
# ─────────────────────────────────────────────────────────────────

@st.cache_resource
def get_supabase_client() -> Client:
    """
    Establish a connection to Supabase using credentials from Streamlit secrets.
    Requires SUPABASE_URL and SUPABASE_KEY in .streamlit/secrets.toml
    """
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except KeyError as e:
        st.error(f"Missing Supabase secret: {e}. Please configure secrets.toml.")
        st.stop()
    except Exception as e:
        st.error(f"Failed to initialize Supabase client: {e}")
        st.stop()

# ─────────────────────────────────────────────────────────────────
# CACHE INVALIDATION UTILITY
# ─────────────────────────────────────────────────────────────────

def clear_db_cache():
    """Clear cached query data after a mutation (Insert/Update/Delete)."""
    st.cache_data.clear()

# ─────────────────────────────────────────────────────────────────
# OPTIMIZED HELPER FUNCTIONS (SUPABASE ORM)
# ─────────────────────────────────────────────────────────────────

def supabase_insert(table: str, data: dict):
    """Insert a single record into a Supabase table."""
    client = get_supabase_client()
    try:
        response = client.table(table).insert(data).execute()
        clear_db_cache()
        return True
    except Exception as e:
        st.error(f"Database Insert Error: {e}")
        return False

@st.cache_data(ttl=600) # Cache for 10 minutes or until invalidated
def supabase_select(table: str, match_filter: dict = None, ilike_filter: dict = None, or_filter: str = None):
    """
    Fetch records from a Supabase table.
    - match_filter: dict of exact matches (e.g. {"id": 1})
    - ilike_filter: dict of partial matches (case-insensitive)
    - or_filter: string for OR logic (e.g. "name.ilike.%John%,profession.ilike.%John%")
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
        return response.data
    except Exception as e:
        st.error(f"Database Fetch Error: {e}")
        return []

def supabase_update(table: str, data: dict, match_filter: dict):
    """Update records in a Supabase table matching the filter."""
    client = get_supabase_client()
    try:
        query = client.table(table).update(data)
        for k, v in match_filter.items():
            query = query.eq(k, v)
        query.execute()
        clear_db_cache()
        return True
    except Exception as e:
        st.error(f"Database Update Error: {e}")
        return False

def supabase_delete(table: str, match_filter: dict):
    """Delete records from a Supabase table matching the filter."""
    client = get_supabase_client()
    try:
        query = client.table(table).delete()
        for k, v in match_filter.items():
            query = query.eq(k, v)
        query.execute()
        clear_db_cache()
        return True
    except Exception as e:
        st.error(f"Database Delete Error: {e}")
        return False