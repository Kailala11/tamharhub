"""
db_supabase.py — Supabase PostgreSQL layer untuk TamharHub
Digunakan sebagai database utama saat di-deploy di Streamlit Cloud.
Fallback ke SQLite jika credentials tidak tersedia (development lokal).
"""
import streamlit as st
import pandas as pd
from datetime import date

SUPABASE_URL = "https://fodvxtulmrzzwtvirpuc.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZvZHZ4dHVsbXJ6end0dmlycHVjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzcyNTY4OTIsImV4cCI6MjA5MjgzMjg5Mn0.kGByHoXbJf2VJlROfa6i8VeI1t1BUVySjvp5zRo4AjQ"


@st.cache_resource
def get_supabase():
    """Return Supabase client, cached per session."""
    try:
        url = st.secrets.get("supabase", {}).get("url", SUPABASE_URL)
        key = st.secrets.get("supabase", {}).get("key", SUPABASE_KEY)
        from supabase import create_client
        client = create_client(url, key)
        return client
    except Exception:
        return None


def is_supabase_available() -> bool:
    return get_supabase() is not None


# ── Helper: Supabase → DataFrame ──────────────────────────────────

def sb_to_df(table: str, select: str = "*", filters: dict = None,
             order: str = None, limit: int = None) -> pd.DataFrame:
    sb = get_supabase()
    if not sb:
        return pd.DataFrame()
    try:
        q = sb.table(table).select(select)
        if filters:
            for col, val in filters.items():
                q = q.eq(col, val)
        if order:
            q = q.order(order)
        if limit:
            q = q.limit(limit)
        res = q.execute()
        return pd.DataFrame(res.data) if res.data else pd.DataFrame()
    except Exception as e:
        st.warning(f"Supabase error: {e}")
        return pd.DataFrame()


def sb_upsert(table: str, data: dict, on_conflict: str = None) -> bool:
    sb = get_supabase()
    if not sb:
        return False
    try:
        if on_conflict:
            sb.table(table).upsert(data, on_conflict=on_conflict).execute()
        else:
            sb.table(table).upsert(data).execute()
        return True
    except Exception as e:
        st.warning(f"Supabase upsert error: {e}")
        return False


def sb_insert(table: str, data: dict) -> bool:
    sb = get_supabase()
    if not sb:
        return False
    try:
        sb.table(table).insert(data).execute()
        return True
    except Exception as e:
        st.warning(f"Supabase insert error: {e}")
        return False


def sb_delete(table: str, filters: dict) -> bool:
    sb = get_supabase()
    if not sb:
        return False
    try:
        q = sb.table(table).delete()
        for col, val in filters.items():
            q = q.eq(col, val)
        q.execute()
        return True
    except Exception as e:
        st.warning(f"Supabase delete error: {e}")
        return False


def sb_count(table: str, filters: dict = None) -> int:
    sb = get_supabase()
    if not sb:
        return 0
    try:
        q = sb.table(table).select("id", count="exact")
        if filters:
            for col, val in filters.items():
                q = q.eq(col, val)
        res = q.execute()
        return res.count or 0
    except Exception:
        return 0
