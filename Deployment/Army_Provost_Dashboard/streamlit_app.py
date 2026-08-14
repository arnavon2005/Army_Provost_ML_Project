
import streamlit as st

from auth import (
    authenticate_operator,
    register_operator
)

from ui_styles import (
    apply_app_styles
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Army Provost Control Room",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# APPLY SHARED VISUAL SYSTEM
# ============================================================

apply_app_styles()


# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "operator_uid" not in st.session_state:
    st.session_state.operator_uid = None

if "operator_name" not in st.session_state:
    st.session_state.operator_name = None


# ============================================================
# LOGOUT
# ============================================================

def logout():

    st.session_state.authenticated = False
    st.session_state.operator_uid = None
    st.session_state.operator_name = None

    st.rerun()


# ============================================================
# AUTHENTICATION PAGE
# ============================================================

def authentication_page():

    st.title("🛡️ CONTROL ROOM")

    st.subheader(
        "Army Provost Decision Support System"
    )

    st.caption(
        "Version 1.1 — College Prototype"
    )

    st.info(
        "Authorized prototype operators must sign in "
        "before accessing the Control Room."
    )

    st.divider()

    sign_in_tab, register_tab = st.tabs(
        [
            "SIGN IN",
            "REGISTER"
        ]
    )


    # ========================================================
    # SIGN IN
    # ========================================================

    with sign_in_tab:

        st.markdown(
            "### Operator Sign In"
        )

        with st.form(
            "operator_sign_in_form"
        ):

            operator_uid = st.text_input(
                "Operator UID",
                placeholder="Enter Operator UID"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter password"
            )

            sign_in_submitted = st.form_submit_button(
                "SIGN IN",
                use_container_width=True
            )

        if sign_in_submitted:

            success, result = authenticate_operator(
                operator_uid,
                password
            )

            if success:

                st.session_state.authenticated = True

                st.session_state.operator_uid = (
                    result["operator_uid"]
                )

                st.session_state.operator_name = (
                    result["display_name"]
                    if result["display_name"]
                    else result["operator_uid"]
                )

                st.success(
                    "Authentication successful."
                )

                st.rerun()

            else:

                st.error(
                    result
                )


    # ========================================================
    # REGISTER
    # ========================================================

    with register_tab:

        st.markdown(
            "### Register Prototype Operator"
        )

        st.caption(
            "Self-registration is enabled only for "
            "this academic prototype."
        )

        with st.form(
            "operator_registration_form"
        ):

            new_display_name = st.text_input(
                "Operator Name",
                placeholder="Enter operator name"
            )

            new_operator_uid = st.text_input(
                "Create Operator UID",
                placeholder="Minimum 3 characters"
            )

            new_password = st.text_input(
                "Create Password",
                type="password",
                placeholder="Minimum 8 characters"
            )

            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                placeholder="Re-enter password"
            )

            register_submitted = st.form_submit_button(
                "REGISTER",
                use_container_width=True
            )

        if register_submitted:

            if new_password != confirm_password:

                st.error(
                    "Passwords do not match."
                )

            else:

                success, message = register_operator(
                    operator_uid=new_operator_uid,
                    password=new_password,
                    display_name=new_display_name
                )

                if success:

                    st.success(
                        message
                        + " You can now sign in using "
                          "your Operator UID."
                    )

                else:

                    st.error(
                        message
                    )


    # ========================================================
    # PROTOTYPE SECURITY NOTICE
    # ========================================================

    st.divider()

    st.caption(
        "Prototype Security Notice: "
        "This authentication system is intended for academic "
        "demonstration only. A real institutional deployment "
        "would require an approved managed identity and "
        "access-control system."
    )


# ============================================================
# DYNAMIC NAVIGATION
# ============================================================

if not st.session_state.authenticated:

    login_page = st.Page(
        authentication_page,
        title="Sign In",
        icon="🔐",
        default=True
    )

    navigation = st.navigation(
        [login_page],
        position="hidden"
    )

    navigation.run()


else:

    # ========================================================
    # AUTHENTICATED PAGE DEFINITIONS
    # ========================================================

    home_page = st.Page(
        "pages/home.py",
        title="Home",
        icon="🏠",
        default=True
    )

    operations_page = st.Page(
        "pages/operations.py",
        title="Operations",
        icon="🛡️"
    )

    response_teams_page = st.Page(
        "pages/response_teams.py",
        title="Response Teams",
        icon="🚓"
    )

    analytics_page = st.Page(
        "pages/analytics.py",
        title="Analytics",
        icon="📊"
    )

    audit_logs_page = st.Page(
        "pages/audit_logs.py",
        title="Audit Logs",
        icon="🗃️"
    )


    # ========================================================
    # PROTECTED NAVIGATION
    # ========================================================

    navigation = st.navigation(
        {
            "Control Room": [
                home_page,
                operations_page,
                response_teams_page
            ],

            "System Intelligence": [
                analytics_page
            ],

            "Records": [
                audit_logs_page
            ]
        }
    )


    # ========================================================
    # AUTHENTICATED SIDEBAR
    # ========================================================

    with st.sidebar:

        st.markdown(
            "## 🛡️ CONTROL ROOM"
        )

        st.caption(
            "Army Provost DSS — Version 1.1"
        )

        st.divider()

        st.markdown(
            "### Operator"
        )

        st.markdown(
            f"**{st.session_state.operator_name}**"
        )

        st.caption(
            f"UID: {st.session_state.operator_uid}"
        )

        st.success(
            "Authenticated Session"
        )

        st.divider()

        st.markdown(
            "### System Status"
        )

        st.success(
            "Decision-Support System Online"
        )

        st.caption(
            "Human authorization remains required "
            "for final operational decisions."
        )

        st.divider()

        st.markdown(
            "### Additional Support"
        )

        st.caption(
            "SIMULATED CONTACTS — Academic Prototype"
        )

        st.markdown(
            """
            **Control Room Support**
            +91 90000 10001

            **Medical Support**
            +91 90000 10002

            **Fire / Emergency**
            +91 90000 10003

            **Duty Supervisor**
            +91 90000 10004
            """
        )

        st.caption(
            "These contact details are fictional and are "
            "not connected to any real military or emergency service."
        )

        st.divider()

        st.markdown(
            "### Session"
        )

        if st.button(
            "LOG OUT",
            use_container_width=True
        ):

            logout()


    # ========================================================
    # RUN SELECTED PROTECTED PAGE
    # ========================================================

    navigation.run()
