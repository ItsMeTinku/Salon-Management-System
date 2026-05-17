"""
auth.py — Authentication & Persistent Session Management (Fixed)
─────────────────────────────────────────────────────────────────
FIX for CachedWidgetWarning:
  CookieManager is a Streamlit widget — it cannot be created inside
  @st.cache_resource or @st.cache_data. Doing so raises:
      CachedWidgetWarning: Your script uses a widget command in a cached function.

  Solution: Create CookieManager at module level on first import, then
  store it in st.session_state so it persists across reruns without
  needing any cache decorator at all.

  This is the correct pattern recommended by the extra-streamlit-components
  library for Streamlit Cloud deployments.
"""

import streamlit as st
import extra_streamlit_components as stx
import hashlib
import hmac
import time
from datetime import datetime, timedelta
from database import supabase_select

# ─── Configuration ────────────────────────────────────────────────
SESSION_DURATION_DAYS = 7
COOKIE_NAME           = "salon_erp_session"
VALID_PAGES           = [
    "Dashboard", "Appointments", "Customers",
    "Billing", "Employees", "Attendance", "Search",
]


# ─── Cookie Manager — NO @st.cache_resource ──────────────────────
def _get_cookie_manager() -> stx.CookieManager:
    """
    Return (or create) the CookieManager, stored in st.session_state.

    WHY session_state instead of cache_resource:
      CookieManager renders a hidden Streamlit component (widget).
      Widgets must be created in the main script flow, not inside
      cached functions. st.session_state survives reruns within the
      same browser session, which is exactly what we need.
    """
    if "_cookie_mgr" not in st.session_state:
        st.session_state._cookie_mgr = stx.CookieManager(
            key="salon_cookie_mgr_v4"
        )
    return st.session_state._cookie_mgr


# ─── Secret Key ──────────────────────────────────────────────────
def _get_secret() -> str:
    try:
        return st.secrets.get(
            "SESSION_SECRET", "salon_erp_fallback_secret_change_me"
        )
    except Exception:
        return "salon_erp_fallback_secret_change_me"


# ─── Token: Create & Verify ──────────────────────────────────────
def _make_token(username: str, role: str) -> str:
    """
    Build an HMAC-SHA256 signed token.
    Format: username|role|unix_ts|signature
    """
    ts      = str(int(time.time()))
    payload = f"{username}|{role}|{ts}"
    sig     = hmac.new(
        _get_secret().encode(),
        payload.encode(),
        hashlib.sha256,
    ).hexdigest()
    return f"{payload}|{sig}"


def _verify_token(token: str) -> dict | None:
    """
    Validate token signature and expiry.
    Returns {"username": ..., "role": ...} on success, None on failure.
    """
    try:
        parts = token.strip().split("|")
        if len(parts) != 4:
            return None

        username, role, ts, sig = parts
        payload  = f"{username}|{role}|{ts}"
        expected = hmac.new(
            _get_secret().encode(),
            payload.encode(),
            hashlib.sha256,
        ).hexdigest()

        # Constant-time compare prevents timing attacks
        if not hmac.compare_digest(sig, expected):
            return None

        # Check expiry
        if int(time.time()) - int(ts) > SESSION_DURATION_DAYS * 86400:
            return None

        return {"username": username, "role": role}
    except Exception:
        return None


# ─── Page Sync ───────────────────────────────────────────────────
def _sync_page_from_url() -> None:
    """Restore the current page from URL query param after a refresh."""
    url_page = st.query_params.get("page", None)
    if url_page and url_page in VALID_PAGES:
        st.session_state.page = url_page


# ─── Session Initialisation ──────────────────────────────────────
def init_session() -> None:
    """
    Called once at the very top of app.py before anything else.

    Flow:
      1. Set missing session_state defaults.
      2. If already logged in this run → just sync page from URL → done.
      3. Create CookieManager (stored in session_state, NOT cached).
      4. Read cookie → verify token → restore session if valid.
      5. If no valid cookie → leave logged_in=False → show login page.
    """
    # ── 1. Defaults ──────────────────────────────────────────────
    defaults = {
        "logged_in":       False,
        "role":            None,
        "username":        None,
        "page":            "Dashboard",
        "subpage":         None,
        "_session_ready":  False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    # ── 2. Already authenticated this run ────────────────────────
    if st.session_state.logged_in and st.session_state._session_ready:
        _sync_page_from_url()
        return

    # ── 3. Create / retrieve CookieManager (outside any cache) ───
    try:
        cookie_manager = _get_cookie_manager()
    except Exception:
        # If cookie manager fails (e.g. browser blocks cookies)
        # just fall through to the login page
        st.session_state.logged_in    = False
        st.session_state._session_ready = True
        return

    # ── 4. Read and verify cookie ────────────────────────────────
    try:
        token = cookie_manager.get(COOKIE_NAME)
        if token:
            user_data = _verify_token(str(token))
            if user_data:
                st.session_state.logged_in     = True
                st.session_state.username      = user_data["username"]
                st.session_state.role          = user_data["role"]
                st.session_state._session_ready = True
                _sync_page_from_url()
                return
    except Exception:
        pass  # Cookie read failed — treat as not logged in

    # ── 5. No valid session found ────────────────────────────────
    st.session_state.logged_in     = False
    st.session_state._session_ready = True


# ─── Login Page ──────────────────────────────────────────────────
def login_page() -> None:
    """Render the login form. On success: write cookie + set session."""

    st.markdown("""
    <div style="text-align:center; padding:2.5rem 0 1.5rem;">
        <div style="font-size:4rem; line-height:1; margin-bottom:0.5rem;">💇</div>
        <h1 style="color:#1e293b; font-size:2rem; margin:0; font-weight:800;">
            Salon ERP
        </h1>
        <p style="color:#64748b; margin-top:0.3rem; font-size:0.95rem;">
            Sign in to continue
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        with st.container(border=True):
            st.markdown(
                "<h3 style='margin-top:0; color:#1e293b;'>🔐 Login</h3>",
                unsafe_allow_html=True,
            )
            username  = st.text_input("Username", placeholder="Enter username",
                                      key="login_user")
            password  = st.text_input("Password", type="password",
                                      placeholder="Enter password",
                                      key="login_pass")
            role      = st.selectbox("Login as", ["Admin", "Staff"],
                                     key="login_role")
            st.markdown("<br/>", unsafe_allow_html=True)

            if st.button("🚀 Sign In", use_container_width=True,
                         type="primary", key="login_submit"):

                if not username.strip() or not password.strip():
                    st.error("Please enter both username and password.")
                    return

                try:
                    users = supabase_select(
                        "admin",
                        match_filter={
                            "username": username.strip(),
                            "password": password.strip(),
                        },
                    )
                    if users:
                        user        = users[0]
                        actual_user = user.get("username", username.strip())
                        actual_role = user.get("role", role)

                        # ── Write session state ──────────────────────
                        st.session_state.logged_in     = True
                        st.session_state.username      = actual_user
                        st.session_state.role          = actual_role
                        st.session_state.page          = "Dashboard"
                        st.session_state._session_ready = True

                        # ── Write cookie ─────────────────────────────
                        try:
                            token          = _make_token(actual_user, actual_role)
                            expires        = datetime.now() + timedelta(
                                days=SESSION_DURATION_DAYS
                            )
                            cookie_manager = _get_cookie_manager()
                            cookie_manager.set(
                                COOKIE_NAME, token, expires_at=expires
                            )
                        except Exception:
                            pass  # Cookie write failed — session still works

                        # ── Write page to URL ────────────────────────
                        st.query_params["page"] = "Dashboard"

                        st.success("✅ Login successful!")
                        st.rerun()

                    else:
                        st.error("❌ Invalid credentials. Please try again.")

                except Exception as e:
                    st.error(f"Login error: {e}")

    st.markdown("""
    <div style="text-align:center; color:#94a3b8;
                font-size:0.75rem; margin-top:1.5rem;">
        🔒 Secure login &nbsp;•&nbsp; Session valid for 7 days
    </div>
    """, unsafe_allow_html=True)


# ─── Logout ──────────────────────────────────────────────────────
def logout() -> None:
    """Clear session state + delete cookie + clean URL → rerun."""

    # Delete cookie first while manager is still accessible
    try:
        cookie_manager = _get_cookie_manager()
        cookie_manager.delete(COOKIE_NAME)
    except Exception:
        pass

    # Clear all session keys
    keys_to_clear = [
        "logged_in", "role", "username", "page",
        "subpage", "_session_ready", "_cookie_mgr",
    ]
    for key in keys_to_clear:
        st.session_state.pop(key, None)

    # Clean URL
    st.query_params.clear()
    st.rerun()
