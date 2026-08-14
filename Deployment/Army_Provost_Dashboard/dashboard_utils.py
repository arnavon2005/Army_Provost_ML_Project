
import csv
import os
import sys
from pathlib import Path

import joblib
import pandas as pd
from database import get_supabase_client
import streamlit as st


# ============================================================
# DEPLOYMENT PROJECT PATHS
# ============================================================

PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent
)

BACKEND_DIR = (
    PROJECT_ROOT
    / "backend"
)

MODELS_DIR = (
    PROJECT_ROOT
    / "models"
)

DATA_DIR = (
    PROJECT_ROOT
    / "data"
)


# ------------------------------------------------------------
# Compatibility aliases used by existing dashboard functions
# ------------------------------------------------------------

OUTPUTS_PATH = str(
    BACKEND_DIR
)

MODELS_PATH = str(
    MODELS_DIR
)

LOGS_PATH = str(
    DATA_DIR
)


MODEL_PATH = str(
    MODELS_DIR
    / "final_random_forest.pkl"
)

PREPROCESSOR_PATH = str(
    MODELS_DIR
    / "preprocessing_pipeline.pkl"
)

# Legacy compatibility variable.
# Hosted audit persistence now uses Supabase.
AUDIT_LOG_PATH = str(
    DATA_DIR
    / "Army_Provost_DSS_Audit_Log.csv"
)


# ------------------------------------------------------------
# Make deployment backend importable
# ------------------------------------------------------------

if str(BACKEND_DIR) not in sys.path:

    sys.path.insert(
        0,
        str(BACKEND_DIR)
    )


# ============================================================
# IMPORT VALIDATED V1.0 BACKEND
# ============================================================

if OUTPUTS_PATH not in sys.path:

    sys.path.insert(
        0,
        OUTPUTS_PATH
    )


from army_provost_dss_backend import (
    execute_dashboard_dss,
    taxonomy_df
)


# ============================================================
# CACHED RESOURCES
# ============================================================

@st.cache_resource
def load_preprocessor():

    return joblib.load(
        PREPROCESSOR_PATH
    )


@st.cache_data
def get_incident_types():

    incident_types = (
        taxonomy_df[
            "Primary Type"
        ]
        .dropna()
        .astype(str)
        .drop_duplicates()
        .sort_values()
        .tolist()
    )

    return incident_types


@st.cache_data
def get_location_categories():

    preprocessor = load_preprocessor()

    # Validated preprocessing structure:
    # categorical -> OneHotEncoder
    # numerical   -> FunctionTransformer
    encoder = (
        preprocessor.named_transformers_[
            "categorical"
        ]
    )

    categorical_columns = [
        "Primary Type",
        "Location Description",
        "Domestic"
    ]

    location_index = (
        categorical_columns.index(
            "Location Description"
        )
    )

    location_categories = [
        str(value)
        for value in encoder.categories_[
            location_index
        ]
    ]

    return location_categories


# ============================================================
# SESSION DECISION HISTORY
# ============================================================

MAX_RECENT_DECISIONS = 20


def initialize_recent_decisions():

    if (
        "recent_decisions"
        not in st.session_state
    ):

        st.session_state[
            "recent_decisions"
        ] = []


def add_recent_decision(
    record
):

    initialize_recent_decisions()

    st.session_state[
        "recent_decisions"
    ].insert(
        0,
        record
    )

    st.session_state[
        "recent_decisions"
    ] = (
        st.session_state[
            "recent_decisions"
        ][
            :MAX_RECENT_DECISIONS
        ]
    )


# ============================================================
# PERSISTENT AUDIT LOGGING
# ============================================================

AUDIT_LOG_FIELDS = [
    "Decision ID",
    "Decision Timestamp",
    "Incident Type",
    "Location Description",
    "Domestic",
    "Year",
    "Month",
    "Day",
    "Hour",
    "District",
    "Beat",
    "Ward",
    "Community Area",
    "Provost Incident Category",
    "Incident Subcategory",
    "Priority",
    "Arrest Probability (%)",
    "ML Assessment",
    "Recommended Response Type",
    "Immediate Operator Guidance",
    "Coordination / Notification",
    "Scene / Evidence Considerations",
    "Escalation / Follow-up",
    "Guidance Status"
]



def append_dss_audit_record(
    audit_record
):
    """
    Persist one DSS incident-analysis audit record
    to Supabase.
    """

    client = get_supabase_client()


    decision_timestamp = audit_record.get(
        "Decision Timestamp",
        None
    )

    if hasattr(
        decision_timestamp,
        "isoformat"
    ):
        decision_timestamp = (
            decision_timestamp.isoformat()
        )


    record = {

        "decision_id":
            audit_record.get(
                "Decision ID"
            ),

        "decision_timestamp":
            decision_timestamp,

        "primary_type":
            audit_record.get(
                "Incident Type"
            ),

        "location_description":
            audit_record.get(
                "Location Description"
            ),

        "domestic":
            audit_record.get(
                "Domestic"
            ),

        "provost_incident_category":
            audit_record.get(
                "Provost Incident Category"
            ),

        "incident_subcategory":
            audit_record.get(
                "Incident Subcategory"
            ),

        "priority":
            audit_record.get(
                "Priority"
            ),

        "arrest_probability":
            (
                float(
                    audit_record.get(
                        "Arrest Probability (%)"
                    )
                ) / 100.0
                if audit_record.get(
                    "Arrest Probability (%)"
                ) is not None
                else None
            ),

        "arrest_probability_percent":
            audit_record.get(
                "Arrest Probability (%)"
            ),

        "arrest_prediction":
            audit_record.get(
                "ML Assessment"
            ),

        "recommended_response_type":
            audit_record.get(
                "Recommended Response Type"
            ),

        "year":
            audit_record.get(
                "Year"
            ),

        "month":
            audit_record.get(
                "Month"
            ),

        "day":
            audit_record.get(
                "Day"
            ),

        "hour":
            audit_record.get(
                "Hour"
            ),

        "district":
            audit_record.get(
                "District"
            ),

        "beat":
            audit_record.get(
                "Beat"
            ),

        "ward":
            audit_record.get(
                "Ward"
            ),

        "community_area":
            audit_record.get(
                "Community Area"
            ),

        "operator_uid":
            audit_record.get(
                "Operator UID"
            )
    }


    (
        client
        .table(
            "dss_incident_audit"
        )
        .upsert(
            record,
            on_conflict="decision_id"
        )
        .execute()
    )

    return True


def execute_operational_analysis(
    *,
    primary_type,
    location_description,
    domestic,
    year,
    month,
    day,
    hour,
    district,
    beat,
    ward,
    community_area
):

    result = execute_dashboard_dss(
        primary_type=primary_type,
        location_description=location_description,
        domestic=domestic,
        year=year,
        month=month,
        day=day,
        hour=hour,
        district=district,
        beat=beat,
        ward=ward,
        community_area=community_area
    )

    dss_result = result[
        "DSS Result"
    ]

    decision = dss_result[
        "Decision"
    ]

    record = dss_result[
        "Decision Record"
    ]

    guidance = dss_result[
        "Response Guidance"
    ]


    recent_record = {

        "Decision ID":
            record[
                "Decision ID"
            ],

        "Timestamp":
            record[
                "Decision Timestamp"
            ],

        "Incident Type":
            decision[
                "Primary Type"
            ],

        "Priority":
            decision[
                "Priority"
            ],

        "Arrest Probability (%)":
            decision[
                "Arrest Probability (%)"
            ],

        "ML Assessment":
            decision[
                "Arrest Prediction"
            ],

        "Recommended Response Type":
            decision[
                "Recommended Response Type"
            ]
    }


    add_recent_decision(
        recent_record
    )


    audit_record = {

        "Decision ID":
            record[
                "Decision ID"
            ],

        "Decision Timestamp":
            record[
                "Decision Timestamp"
            ],

        "Incident Type":
            decision[
                "Primary Type"
            ],

        "Location Description":
            location_description,

        "Domestic":
            domestic,

        "Year":
            year,

        "Month":
            month,

        "Day":
            day,

        "Hour":
            hour,

        "District":
            district,

        "Beat":
            beat,

        "Ward":
            ward,

        "Community Area":
            community_area,

        "Provost Incident Category":
            decision[
                "Provost Incident Category"
            ],

        "Incident Subcategory":
            decision[
                "Incident Subcategory"
            ],

        "Priority":
            decision[
                "Priority"
            ],

        "Arrest Probability (%)":
            decision[
                "Arrest Probability (%)"
            ],

        "ML Assessment":
            decision[
                "Arrest Prediction"
            ],

        "Recommended Response Type":
            decision[
                "Recommended Response Type"
            ],

        "Immediate Operator Guidance":
            guidance[
                "Immediate Operator Guidance"
            ],

        "Coordination / Notification":
            guidance[
                "Coordination / Notification"
            ],

        "Scene / Evidence Considerations":
            guidance[
                "Scene / Evidence Considerations"
            ],

        "Escalation / Follow-up":
            guidance[
                "Escalation / Follow-up"
            ],

        "Guidance Status":
            guidance[
                "Guidance Status"
            ]
    }


    audit_saved = True
    audit_error = None


    try:

        append_dss_audit_record(
            audit_record
        )

    except Exception as exc:

        audit_saved = False
        audit_error = str(
            exc
        )


    return {
        "Raw Result":
            result,

        "Decision":
            decision,

        "Decision Record":
            record,

        "Response Guidance":
            guidance,

        "Audit Saved":
            audit_saved,

        "Audit Error":
            audit_error
    }



# ============================================================
# RESPONSE TEAM RESOURCE ALLOCATION BACKEND
# ============================================================

from response_team_allocation_backend import (
    load_response_team_registry,
    allocate_response_resource,
    process_operator_decision,
    save_response_team_registry,
    append_resource_allocation_audit
)


# ============================================================
# RESOURCE ALLOCATION WRAPPER
# ============================================================

def execute_resource_allocation(
    *,
    operational_response,
    incident_zone
):
    """
    Run the response-team allocation layer using the
    operational response produced by the existing DSS.
    """

    team_registry = (
        load_response_team_registry()
    )

    allocation_result = (
        allocate_response_resource(
            operational_response=operational_response,
            incident_zone=incident_zone,
            team_registry=team_registry
        )
    )

    return {
        "Team Registry":
            team_registry,

        "Allocation Result":
            allocation_result
    }


# ============================================================
# HUMAN RESOURCE DECISION WRAPPER
# ============================================================

def execute_resource_decision(
    *,
    allocation_result,
    team_registry,
    operator_uid,
    action,
    incident_id,
    selected_team_id=None,
    override_reason=None
):
    """
    Process operator CONFIRM / OVERRIDE decision,
    persist the updated team state,
    and append the allocation audit record.
    """

    decision_record, updated_registry = (
        process_operator_decision(
            allocation_result=allocation_result,
            team_registry=team_registry,
            operator_uid=operator_uid,
            action=action,
            selected_team_id=selected_team_id,
            override_reason=override_reason,
            incident_id=incident_id
        )
    )

    # Persist updated resource state
    save_response_team_registry(
        updated_registry
    )

    # Persist resource allocation audit
    append_resource_allocation_audit(
        decision_record
    )

    return {
        "Decision Record":
            decision_record,

        "Updated Registry":
            updated_registry
    }
