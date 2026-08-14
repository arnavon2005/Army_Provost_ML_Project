
import streamlit as st

from supabase import (
    create_client,
    Client
)


# ============================================================
# SUPABASE CLIENT
# ============================================================

@st.cache_resource
def get_supabase_client() -> Client:
    """
    Create and cache the server-side Supabase client.

    Credentials are loaded exclusively from Streamlit Secrets.
    They must never be hard-coded in source code.
    """

    try:

        supabase_url = st.secrets[
            "SUPABASE_URL"
        ]

        supabase_secret_key = st.secrets[
            "SUPABASE_SECRET_KEY"
        ]

    except KeyError as exc:

        raise RuntimeError(
            "Supabase credentials are not configured. "
            "Expected SUPABASE_URL and "
            "SUPABASE_SECRET_KEY in Streamlit Secrets."
        ) from exc


    if not supabase_url:

        raise RuntimeError(
            "SUPABASE_URL is empty."
        )


    if not supabase_secret_key:

        raise RuntimeError(
            "SUPABASE_SECRET_KEY is empty."
        )


    client = create_client(
        supabase_url,
        supabase_secret_key
    )

    return client


# ============================================================
# CONNECTION TEST
# ============================================================

def test_database_connection():
    """
    Verify that the server-side Supabase client can access
    the Army Provost deployment tables.
    """

    client = get_supabase_client()

    response = (
        client
        .table("response_teams")
        .select(
            "team_id",
            count="exact"
        )
        .limit(1)
        .execute()
    )

    return {
        "Connection": True,
        "Response_Team_Count":
            response.count
    }
