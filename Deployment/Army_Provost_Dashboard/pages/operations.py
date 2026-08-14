
import streamlit as st

from dashboard_utils import (
    execute_operational_analysis,
    execute_resource_allocation,
    execute_resource_decision,
    get_incident_types,
    get_location_categories,
    initialize_recent_decisions
)


# ============================================================
# PAGE INITIALIZATION
# ============================================================

initialize_recent_decisions()

incident_types = get_incident_types()
location_categories = get_location_categories()


# Persistent case state is required because Streamlit reruns
# when the operator presses CONFIRM / OVERRIDE.

if "operations_case" not in st.session_state:
    st.session_state.operations_case = None

if "operations_resource_decision" not in st.session_state:
    st.session_state.operations_resource_decision = None


# ============================================================
# PAGE HEADER
# ============================================================

st.title(
    "🛡️ Operations"
)

st.caption(
    "Incident Assessment & Response Resource Allocation"
)

st.info(
    "Enter the reported incident details. "
    "The system combines the existing ML/DSS assessment "
    "with the simulated response-team registry to recommend "
    "a suitable currently available resource."
)


# ============================================================
# 01 — INCIDENT DETAILS
# ============================================================

st.subheader(
    "01 · Incident Details"
)

col1, col2, col3 = st.columns(
    [1.2, 1.6, 0.8]
)


with col1:

    default_incident_index = (
        incident_types.index("BATTERY")
        if "BATTERY" in incident_types
        else 0
    )

    primary_type = st.selectbox(
        "Incident Type",
        options=incident_types,
        index=default_incident_index
    )


with col2:

    default_location_index = (
        location_categories.index("STREET")
        if "STREET" in location_categories
        else 0
    )

    location_description = st.selectbox(
        "Location Description",
        options=location_categories,
        index=default_location_index
    )


with col3:

    domestic = st.selectbox(
        "Domestic Incident",
        options=[
            False,
            True
        ],
        format_func=lambda value: (
            "Yes"
            if value
            else "No"
        )
    )


# ============================================================
# 02 — OPERATIONAL ZONE
# ============================================================

st.subheader(
    "02 · Simulated Operational Zone"
)

incident_zone = st.selectbox(
    "Incident Zone",
    options=[
        "Zone A",
        "Zone B",
        "Zone C",
        "Zone D",
        "Zone E",
        "Zone F",
        "Zone G",
        "Zone H"
    ],
    index=1,
    help=(
        "Fictional operator-facing zone used only for "
        "prototype resource allocation. It is not a real "
        "military installation location."
    )
)

st.caption(
    "SIMULATED LOCATION DATA — Zones A–H are fictional "
    "and contain no real installation coordinates."
)


# ============================================================
# 03 — DATE & TIME
# ============================================================

st.subheader(
    "03 · Date & Time"
)

col1, col2, col3, col4 = st.columns(4)


with col1:

    year = st.number_input(
        "Year",
        min_value=2001,
        max_value=2100,
        value=2025,
        step=1
    )


with col2:

    month = st.number_input(
        "Month",
        min_value=1,
        max_value=12,
        value=7,
        step=1
    )


with col3:

    day = st.number_input(
        "Day",
        min_value=1,
        max_value=31,
        value=15,
        step=1
    )


with col4:

    hour = st.number_input(
        "Hour",
        min_value=0,
        max_value=23,
        value=20,
        step=1
    )


# ============================================================
# 04 — MODEL COMPATIBILITY INPUTS
# ============================================================

with st.expander(
    "04 · Model Compatibility Inputs"
):

    st.caption(
        "These Chicago-derived administrative fields are retained "
        "only because they are required by the currently trained "
        "Random Forest model. They are not presented as Army "
        "installation geography."
    )

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        district = st.number_input(
            "District",
            min_value=0,
            value=1,
            step=1
        )


    with col2:

        beat = st.number_input(
            "Beat",
            min_value=0,
            value=100,
            step=1
        )


    with col3:

        ward = st.number_input(
            "Ward",
            min_value=0,
            value=1,
            step=1
        )


    with col4:

        community_area = st.number_input(
            "Community Area",
            min_value=0,
            value=32,
            step=1
        )


st.divider()


# ============================================================
# ANALYZE INCIDENT
# ============================================================

analyze_button = st.button(
    "ANALYZE INCIDENT",
    type="primary",
    use_container_width=True
)


if analyze_button:

    try:

        # ----------------------------------------------------
        # Existing ML + DSS
        # ----------------------------------------------------

        analysis = execute_operational_analysis(
            primary_type=primary_type,
            location_description=location_description,
            domestic=domestic,
            year=int(year),
            month=int(month),
            day=int(day),
            hour=int(hour),
            district=int(district),
            beat=int(beat),
            ward=int(ward),
            community_area=int(
                community_area
            )
        )

        decision = analysis[
            "Decision"
        ]

        record = analysis[
            "Decision Record"
        ]

        guidance = analysis[
            "Response Guidance"
        ]


        # ----------------------------------------------------
        # New Resource Allocation Layer
        # ----------------------------------------------------

        resource_result = execute_resource_allocation(
            operational_response=decision[
                "Recommended Response Type"
            ],
            incident_zone=incident_zone
        )

        allocation = resource_result[
            "Allocation Result"
        ]


        # ----------------------------------------------------
        # Store complete case for Streamlit reruns
        # ----------------------------------------------------

        st.session_state.operations_case = {
            "Analysis": analysis,
            "Decision": decision,
            "Decision Record": record,
            "Response Guidance": guidance,
            "Incident Zone": incident_zone,
            "Team Registry": resource_result[
                "Team Registry"
            ],
            "Allocation Result": allocation
        }

        st.session_state.operations_resource_decision = None

        st.success(
            "Incident analyzed and available response "
            "resources evaluated successfully."
        )

    except Exception as exc:

        st.session_state.operations_case = None

        st.error(
            "Incident analysis could not be completed."
        )

        st.exception(
            exc
        )


# ============================================================
# DISPLAY ACTIVE CASE
# ============================================================

case = st.session_state.operations_case


if case is not None:

    analysis = case[
        "Analysis"
    ]

    decision = case[
        "Decision"
    ]

    record = case[
        "Decision Record"
    ]

    guidance = case[
        "Response Guidance"
    ]

    allocation = case[
        "Allocation Result"
    ]

    team_registry = case[
        "Team Registry"
    ]

    active_incident_zone = case[
        "Incident Zone"
    ]


    # ========================================================
    # 05 — OPERATIONAL ASSESSMENT
    # ========================================================

    st.subheader(
        "05 · Operational Assessment"
    )

    priority = decision[
        "Priority"
    ]

    col1, col2, col3 = st.columns(3)


    with col1:

        st.caption(
            "PRIORITY"
        )

        if priority == "Critical":

            st.error(
                "CRITICAL"
            )

        elif priority == "High":

            st.warning(
                "HIGH"
            )

        elif priority == "Moderate":

            st.info(
                "MODERATE"
            )

        else:

            st.success(
                str(priority).upper()
            )


    with col2:

        st.caption(
            "PROVOST CATEGORY"
        )

        st.markdown(
            "### "
            + decision[
                "Provost Incident Category"
            ]
        )


    with col3:

        st.caption(
            "INCIDENT SUBCATEGORY"
        )

        st.markdown(
            "### "
            + decision[
                "Incident Subcategory"
            ]
        )


    st.caption(
        "Mapped response pathway: "
        + decision[
            "Recommended Response Type"
        ]
    )


    # ========================================================
    # 06 — RESPONSE TEAM RECOMMENDATION
    # ========================================================

    st.subheader(
        "06 · Recommended Deployment"
    )

    st.caption(
        "The recommendation below is generated from the "
        "current simulated resource state. Final assignment "
        "requires operator confirmation."
    )


    primary_team = allocation[
        "Primary_Recommendation"
    ]

    alternate_team = allocation[
        "Alternate_Recommendation"
    ]


    if primary_team is None:

        st.error(
            "NO SUITABLE RESPONSE TEAM IS CURRENTLY DEPLOYABLE."
        )

        st.warning(
            "Operator action is required. The system will not "
            "fabricate or automatically force a resource assignment."
        )


    else:

        primary_col, alternate_col = st.columns(
            [1.2, 1]
        )


        with primary_col:

            with st.container(
                border=True
            ):

                st.markdown(
                    "### Primary Recommendation"
                )

                st.markdown(
                    "## "
                    + primary_team[
                        "Team_Name"
                    ]
                )

                st.caption(
                    primary_team[
                        "Team_ID"
                    ]
                )

                metric1, metric2 = st.columns(2)

                with metric1:

                    st.metric(
                        "Suitability Score",
                        (
                            f"{primary_team['Suitability_Score']}/100"
                        )
                    )

                with metric2:

                    st.metric(
                        "Current Zone",
                        primary_team[
                            "Current_Zone"
                        ]
                    )

                st.write(
                    "**Capability Match:** "
                    + primary_team[
                        "Capability_Match"
                    ]
                )

                st.write(
                    "**Readiness:** "
                    + primary_team[
                        "Readiness_Level"
                    ]
                )

                st.write(
                    "**Incident Zone:** "
                    + active_incident_zone
                )


        with alternate_col:

            with st.container(
                border=True
            ):

                st.markdown(
                    "### Alternate Resource"
                )

                if alternate_team is not None:

                    st.markdown(
                        "## "
                        + alternate_team[
                            "Team_Name"
                        ]
                    )

                    st.caption(
                        alternate_team[
                            "Team_ID"
                        ]
                    )

                    st.metric(
                        "Suitability Score",
                        (
                            f"{alternate_team['Suitability_Score']}/100"
                        )
                    )

                    st.write(
                        "**Current Zone:** "
                        + alternate_team[
                            "Current_Zone"
                        ]
                    )

                    st.write(
                        "**Readiness:** "
                        + alternate_team[
                            "Readiness_Level"
                        ]
                    )

                else:

                    st.info(
                        "No alternate deployable resource "
                        "is currently available."
                    )


        # ====================================================
        # 07 — OPERATOR DECISION
        # ====================================================

        st.subheader(
            "07 · Operator Decision"
        )

        existing_resource_decision = (
            st.session_state.operations_resource_decision
        )


        if existing_resource_decision is None:

            st.warning(
                "The DSS recommendation is advisory. "
                "The authorized operator must CONFIRM the "
                "recommended team or OVERRIDE it with another "
                "eligible resource."
            )


            confirm_col, override_col = st.columns(2)


            # ------------------------------------------------
            # CONFIRM
            # ------------------------------------------------

            with confirm_col:

                if st.button(
                    "CONFIRM RECOMMENDED TEAM",
                    type="primary",
                    use_container_width=True,
                    key="confirm_resource_team"
                ):

                    try:

                        resource_decision = (
                            execute_resource_decision(
                                allocation_result=allocation,
                                team_registry=team_registry,
                                operator_uid=st.session_state.get(
                                    "operator_uid",
                                    "UNKNOWN"
                                ),
                                action="CONFIRM",
                                incident_id=record[
                                    "Decision ID"
                                ]
                            )
                        )

                        st.session_state.operations_resource_decision = (
                            resource_decision
                        )

                        st.success(
                            "Recommended response team assigned."
                        )

                        st.rerun()

                    except Exception as exc:

                        st.error(
                            "Team assignment could not be completed."
                        )

                        st.exception(
                            exc
                        )


            # ------------------------------------------------
            # OVERRIDE
            # ------------------------------------------------

            with override_col:

                ranking = allocation[
                    "Full_Ranking"
                ]

                override_options = (
                    ranking[
                        ranking["Team_ID"]
                        != primary_team[
                            "Team_ID"
                        ]
                    ][
                        "Team_ID"
                    ]
                    .tolist()
                )


                if override_options:

                    selected_override_team = st.selectbox(
                        "Override Resource",
                        options=override_options,
                        key="override_resource_selection"
                    )

                    override_reason = st.text_area(
                        "Override Reason",
                        placeholder=(
                            "Enter the operational reason for "
                            "selecting an alternate eligible team."
                        ),
                        key="override_resource_reason"
                    )

                    if st.button(
                        "OVERRIDE RECOMMENDATION",
                        use_container_width=True,
                        key="override_resource_team"
                    ):

                        try:

                            resource_decision = (
                                execute_resource_decision(
                                    allocation_result=allocation,
                                    team_registry=team_registry,
                                    operator_uid=st.session_state.get(
                                        "operator_uid",
                                        "UNKNOWN"
                                    ),
                                    action="OVERRIDE",
                                    selected_team_id=(
                                        selected_override_team
                                    ),
                                    override_reason=(
                                        override_reason
                                    ),
                                    incident_id=record[
                                        "Decision ID"
                                    ]
                                )
                            )

                            st.session_state.operations_resource_decision = (
                                resource_decision
                            )

                            st.success(
                                "Operator override recorded and "
                                "selected response team assigned."
                            )

                            st.rerun()

                        except Exception as exc:

                            st.error(
                                "Override could not be completed."
                            )

                            st.exception(
                                exc
                            )

                else:

                    st.info(
                        "No alternate eligible team is available "
                        "for operator override."
                    )


        else:

            final_record = existing_resource_decision[
                "Decision Record"
            ]

            st.success(
                "RESOURCE ASSIGNMENT RECORDED"
            )

            col1, col2, col3 = st.columns(3)


            with col1:

                st.caption(
                    "RECOMMENDED TEAM"
                )

                st.markdown(
                    "### "
                    + final_record[
                        "Recommended_Team_ID"
                    ]
                )


            with col2:

                st.caption(
                    "FINAL SELECTED TEAM"
                )

                st.markdown(
                    "### "
                    + final_record[
                        "Selected_Team_ID"
                    ]
                )


            with col3:

                st.caption(
                    "OPERATOR ACTION"
                )

                st.markdown(
                    "### "
                    + final_record[
                        "Operator_Action"
                    ]
                )


            if final_record[
                "Override_Reason"
            ]:

                st.info(
                    "Override Reason: "
                    + final_record[
                        "Override_Reason"
                    ]
                )


            st.caption(
                "Allocation Decision ID: "
                + final_record[
                    "Decision_ID"
                ]
            )

            st.caption(
                "Resource allocation audit record saved."
            )


    # ========================================================
    # 08 — RESPONSE REFERENCE
    # ========================================================

    with st.expander(
        "08 · Response Reference / Prototype Guidance"
    ):

        st.caption(
            "This material is secondary decision-support "
            "reference information and is not represented "
            "as an official operational SOP."
        )


        st.markdown(
            "**Immediate Operator Guidance**"
        )

        st.write(
            guidance[
                "Immediate Operator Guidance"
            ]
        )


        st.markdown(
            "**Coordination / Notification**"
        )

        st.write(
            guidance[
                "Coordination / Notification"
            ]
        )


        st.markdown(
            "**Scene / Evidence Considerations**"
        )

        st.write(
            guidance[
                "Scene / Evidence Considerations"
            ]
        )


        st.markdown(
            "**Escalation / Follow-up**"
        )

        st.write(
            guidance[
                "Escalation / Follow-up"
            ]
        )


    # ========================================================
    # 09 — TECHNICAL MODEL CONTEXT
    # ========================================================

    with st.expander(
        "09 · Technical Model Context"
    ):

        st.caption(
            "The Random Forest output is a historical "
            "arrest-outcome context signal. It does not "
            "authorize an arrest and does not independently "
            "determine resource deployment."
        )

        col1, col2 = st.columns(2)


        with col1:

            st.metric(
                "Historical Arrest Outcome Likelihood",
                (
                    f"{decision['Arrest Probability (%)']:.2f}%"
                )
            )


        with col2:

            st.metric(
                "Current Model Classification",
                decision[
                    "Arrest Prediction"
                ]
            )


    # ========================================================
    # 10 — INCIDENT DECISION RECORD
    # ========================================================

    st.subheader(
        "10 · Incident Decision Record"
    )

    col1, col2 = st.columns(2)


    with col1:

        st.caption(
            "DECISION ID"
        )

        st.code(
            record[
                "Decision ID"
            ],
            language=None
        )


    with col2:

        st.caption(
            "DECISION TIMESTAMP"
        )

        st.code(
            record[
                "Decision Timestamp"
            ],
            language=None
        )


    if analysis[
        "Audit Saved"
    ]:

        st.caption(
            "✓ Incident DSS audit record saved."
        )

    else:

        st.warning(
            "Incident analysis succeeded, but the DSS "
            "audit record could not be saved."
        )


    # ========================================================
    # HUMAN OVERSIGHT
    # ========================================================

    st.warning(
        "Human Oversight Requirement: "
        "ML outputs and response-team recommendations are "
        "decision-support information only. Final operational "
        "resource assignment remains with the authorized operator."
    )
