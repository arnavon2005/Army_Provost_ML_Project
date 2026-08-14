
import streamlit as st

from response_team_allocation_backend import (
    load_response_team_registry,
    release_response_team,
    save_response_team_registry
)


# ======================================================================
# PAGE HEADER
# ======================================================================

st.title(
    "🚓 Response Teams"
)

st.caption(
    "Simulated Response Resource Status & Availability"
)

st.info(
    "All response-team information shown on this page is synthetic "
    "and exists only for academic prototype demonstration."
)


# ======================================================================
# LOAD CURRENT REGISTRY
# ======================================================================

try:

    team_registry = (
        load_response_team_registry()
    )

except Exception as exc:

    st.error(
        "The Response Team Registry could not be loaded."
    )

    st.exception(
        exc
    )

    st.stop()


# ======================================================================
# SUMMARY METRICS
# ======================================================================

st.subheader(
    "01 · Resource Status"
)

total_teams = len(
    team_registry
)

available_teams = (
    team_registry["Status"]
    .eq("AVAILABLE")
    .sum()
)

assigned_teams = (
    team_registry["Status"]
    .eq("ASSIGNED")
    .sum()
)

offline_teams = (
    team_registry["Status"]
    .eq("OFFLINE")
    .sum()
)


col1, col2, col3, col4 = (
    st.columns(4)
)


with col1:

    st.metric(
        "Total Teams",
        int(total_teams)
    )


with col2:

    st.metric(
        "Available",
        int(available_teams)
    )


with col3:

    st.metric(
        "Assigned",
        int(assigned_teams)
    )


with col4:

    st.metric(
        "Offline",
        int(offline_teams)
    )


st.divider()


# ======================================================================
# CURRENT RESOURCE REGISTRY
# ======================================================================

st.subheader(
    "02 · Response Team Registry"
)


display_columns = [
    "Team_ID",
    "Team_Name",
    "Status",
    "Current_Zone",
    "Primary_Capability",
    "Secondary_Capabilities",
    "Readiness_Level",
    "Personnel_Strength",
    "Vehicle_Available",
    "Current_Assignment"
]


st.dataframe(
    team_registry[
        display_columns
    ],
    use_container_width=True,
    hide_index=True
)


st.caption(
    "Availability and readiness are separate states. "
    "An AVAILABLE team may still have LIMITED readiness."
)


st.divider()


# ======================================================================
# STATUS GROUPS
# ======================================================================

st.subheader(
    "03 · Operational Availability"
)


available_tab, assigned_tab, offline_tab = (
    st.tabs(
        [
            "AVAILABLE",
            "ASSIGNED",
            "OFFLINE"
        ]
    )
)


# ----------------------------------------------------------------------
# AVAILABLE
# ----------------------------------------------------------------------

with available_tab:

    available_df = team_registry[
        team_registry["Status"]
        == "AVAILABLE"
    ]

    if available_df.empty:

        st.warning(
            "No teams are currently available."
        )

    else:

        st.dataframe(
            available_df[
                [
                    "Team_ID",
                    "Team_Name",
                    "Current_Zone",
                    "Primary_Capability",
                    "Readiness_Level",
                    "Personnel_Strength",
                    "Vehicle_Available"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )


# ----------------------------------------------------------------------
# ASSIGNED
# ----------------------------------------------------------------------

with assigned_tab:

    assigned_df = team_registry[
        team_registry["Status"]
        == "ASSIGNED"
    ]

    if assigned_df.empty:

        st.success(
            "No response teams are currently assigned."
        )

    else:

        st.dataframe(
            assigned_df[
                [
                    "Team_ID",
                    "Team_Name",
                    "Current_Zone",
                    "Primary_Capability",
                    "Readiness_Level",
                    "Current_Assignment"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )


# ----------------------------------------------------------------------
# OFFLINE
# ----------------------------------------------------------------------

with offline_tab:

    offline_df = team_registry[
        team_registry["Status"]
        == "OFFLINE"
    ]

    if offline_df.empty:

        st.success(
            "No teams are currently offline."
        )

    else:

        st.dataframe(
            offline_df[
                [
                    "Team_ID",
                    "Team_Name",
                    "Current_Zone",
                    "Primary_Capability",
                    "Readiness_Level",
                    "Vehicle_Available"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )


st.divider()


# ======================================================================
# RELEASE ASSIGNED RESOURCE
# ======================================================================

st.subheader(
    "04 · Release Assigned Team"
)


assigned_team_ids = (
    team_registry.loc[
        team_registry["Status"]
        == "ASSIGNED",
        "Team_ID"
    ]
    .tolist()
)


if not assigned_team_ids:

    st.info(
        "There are currently no assigned teams to release."
    )

else:

    st.warning(
        "Release a team only after its simulated assignment "
        "has been completed or otherwise cleared by the operator."
    )

    selected_team_id = st.selectbox(
        "Assigned Team",
        options=assigned_team_ids
    )

    selected_team = team_registry[
        team_registry["Team_ID"]
        == selected_team_id
    ].iloc[0]

    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Team",
            selected_team[
                "Team_ID"
            ]
        )


    with col2:

        st.metric(
            "Zone",
            selected_team[
                "Current_Zone"
            ]
        )


    with col3:

        current_assignment = (
            selected_team[
                "Current_Assignment"
            ]
        )

        st.metric(
            "Assignment",
            (
                str(current_assignment)
                if str(current_assignment).lower()
                != "nan"
                else "Not Recorded"
            )
        )


    release_confirmation = (
        st.checkbox(
            "I confirm that this simulated assignment "
            "is complete and the team may be released."
        )
    )


    if st.button(
        "RELEASE TEAM",
        type="primary",
        use_container_width=True,
        disabled=not release_confirmation
    ):

        try:

            updated_registry = (
                release_response_team(
                    team_registry,
                    selected_team_id
                )
            )

            save_response_team_registry(
                updated_registry
            )

            st.success(
                f"{selected_team_id} released successfully "
                "and returned to AVAILABLE status."
            )

            st.rerun()

        except Exception as exc:

            st.error(
                "The selected response team could not be released."
            )

            st.exception(
                exc
            )


# ======================================================================
# HUMAN OVERSIGHT
# ======================================================================

st.warning(
    "All resource states and assignments are simulated. "
    "This page does not represent real military units, "
    "deployment status, or operational locations."
)
