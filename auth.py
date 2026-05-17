"""
auth.py — Authentication & Persistent Session Management
─────────────────────────────────────────────────────────
CHANGES FROM V3:
  1. PERSISTENT LOGIN via extra-streamlit-components CookieManager.
     On login, a signed HMAC token is stored in a browser cookie.
     On every app load, the token is verified and session is restored
     automatically — user stays logged in across browser refreshes.

  2. SECURE TOKENS: The session token is HMAC-SHA256 signed with a
     secret key (from secrets.toml). It encodes username, role, and
     timestamp. An expired or tampered token is rejected.

  3. SESSION EXPIRY: Tokens expire after SESSION_DURATION_DAYS (7 days
     by default). The user must re-login after expiry.

  4. PAGE PERSISTENCE: The last visited page is stored in st.query_params
     (URL), which survives browser refresh natively without any extra lib.

  5. SECURE LOGOUT: Clears both the session state and the cookie, plus
     cleans up the URL query params.
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
COOKIE_NAME = "salon_erp_token"
VALID_PAGES = [
    "Dashboard", "Appointments", "Customers",
    "Billing", "Employees", "Attendance", "Search"
]

# ─── Cookie Manager ──────────────────────────────────────────────
def _get_cookie_manager() -> stx.CookieManager:
    """Return CookieManager instance."""
    return stx.CookieManager(key="salon_erp_cookie_mgr_v4")


# ─── Token Utilities ─────────────────────────────────────────────

def _get_secret() -> str:
    """Read signing secret from Streamlit secrets or use a fallback."""
    try:
        return st.secrets.get("SESSION_SECRET", "salon_erp_change_this_secret_2024")
    except Exception:
        return "salon_erp_change_this_secret_2024"


def _make_token(username: str, role: str) -> str:
    """
    Create an HMAC-signed session token.
    Format: username|role|unix_timestamp|hex_signature
    """
    ts = str(int(time.time()))
    payload = f"{username}|{role}|{ts}"
    sig = hmac.new(
        _get_secret().encode("utf-8"),
        payload.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return f"{payload}|{sig}"


def _verify_token(token: str) -> dict | None:
    """
    Validate an HMAC token. Returns {'username': ..., 'role': ...} on
    success, or None if the token is invalid, tampered, or expired.
    """
    try:
        parts = token.split("|")
        if len(parts) != 4:
            return None
        username, role, ts, sig = parts
        payload = f"{username}|{role}|{ts}"
        expected = hmac.new(
            _get_secret().encode("utf-8"),
            payload.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        # Constant-time comparison prevents timing attacks
        if not hmac.compare_digest(sig, expected):
            return None
        # Check expiry
        age_seconds = int(time.time()) - int(ts)
        if age_seconds > SESSION_DURATION_DAYS * 86400:
            return None
        return {"username": username, "role": role}
    except Exception:
        return None


# ─── Session Initialization ───────────────────────────────────────

def init_session() -> None:
    """
    Called once at the very top of app.py.

    Priority order for session state:
      1. Already logged in this run (st.session_state) → skip all checks.
      2. Valid cookie found → restore session silently.
      3. No valid cookie → show login page (handled by caller).

    Page restoration:
      st.query_params["page"] is preserved across browser refreshes
      because it lives in the URL. We read it here and sync it to
      st.session_state.page after auth is confirmed.
    """
    # Set defaults once
    defaults = {
        "logged_in": False,
        "role": None,
        "username": None,
        "page": "Dashboard",
        "subpage": None,
        "_cookie_checked": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    # Already authenticated in this browser session — nothing to do
    if st.session_state.logged_in and st.session_state._cookie_checked:
        _sync_page_from_url()
        return

    # ── Attempt cookie-based restoration ────────────────────────
    cookie_manager = _get_cookie_manager()
    token = cookie_manager.get(COOKIE_NAME)
    st.session_state._cookie_checked = True

    if token:
        user_data = _verify_token(str(token))
        if user_data:
            st.session_state.logged_in = True
            st.session_state.username = user_data["username"]
            st.session_state.role = user_data["role"]
            _sync_page_from_url()
            return

    # Cookie absent or invalid — session stays logged_out
    st.session_state.logged_in = False


def _sync_page_from_url() -> None:
    """Read ?page=X from URL and update session state if valid."""
    url_page = st.query_params.get("page", None)
    if url_page and url_page in VALID_PAGES:
        st.session_state.page = url_page


# ─── Login Page ───────────────────────────────────────────────────

def login_page() -> None:
    """Render the login form. Sets cookie and session on success."""

    # ── Page chrome ─────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center; padding: 2rem 0 1rem;">
        <div style="font-size: 4rem; margin-bottom: 0.5rem;">💇</div>
        <h1 style="color:#1e293b; font-size: 2rem; margin:0;">Salon ERP</h1>
        <p style="color:#64748b; margin-top: 0.25rem;">Sign in to continue</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        with st.container(border=True):
            st.markdown("<h3 style='margin-top:0; color:#1e293b;'>🔐 Login</h3>",
                        unsafe_allow_html=True)
            username = st.text_input("Username", placeholder="Enter username",
                                     key="login_user")
            password = st.text_input("Password", type="password",
                                     placeholder="Enter password", key="login_pass")
            role     = st.selectbox("Login as", ["Admin", "Staff"],
                                    key="login_role")

            st.markdown("<br/>", unsafe_allow_html=True)
            login_btn = st.button("🚀 Sign In", use_container_width=True,
                                  type="primary", key="login_submit")

            if login_btn:
                if not username.strip() or not password.strip():
                    st.error("Please enter both username and password.")
                    return
                try:
                    users = supabase_select(
                        "admin",
                        match_filter={"username": username.strip(),
                                      "password": password.strip()}
                    )
                    if users:
                        user = users[0]
                        actual_role = user.get("role", role)
                        actual_user = user.get("username", username.strip())

                        # ── Persist to session ───────────────────────
                        st.session_state.logged_in = True
                        st.session_state.username  = actual_user
                        st.session_state.role      = actual_role
                        st.session_state.page      = "Dashboard"
                        st.session_state._cookie_checked = True

                        # ── Persist to cookie ────────────────────────
                        token = _make_token(actual_user, actual_role)
                        expires = datetime.now() + timedelta(days=SESSION_DURATION_DAYS)
                        cookie_manager = _get_cookie_manager()
                        cookie_manager.set(COOKIE_NAME, token, expires_at=expires)

                        # ── Update URL ────────────────────────────────
                        st.query_params["page"] = "Dashboard"

                        st.success("✅ Login successful! Loading dashboard…")
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials. Please try again.")
                except Exception as e:
                    st.error(f"Login error: {e}")

    # Footer
    st.markdown("""
    <div style="text-align:center; color:#94a3b8; font-size:0.75rem; margin-top:2rem;">
        Secure login • Session valid for 7 days
    </div>
    """, unsafe_allow_html=True)


# ─── Logout ───────────────────────────────────────────────────────

def logout() -> None:
    """Clear session state, delete cookie, clean URL, rerun."""
    # Clear session
    for key in ["logged_in", "role", "username", "page",
                 "subpage", "_cookie_checked"]:
        st.session_state.pop(key, None)

    # Delete cookie
    try:
        cookie_manager = _get_cookie_manager()
        cookie_manager.delete(COOKIE_NAME)
    except Exception:
        pass  # Cookie might not exist — that's fine

    # Clean URL
    st.query_params.clear()

    st.rerun()
