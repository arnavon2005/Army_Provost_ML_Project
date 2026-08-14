
# ======================================================================
# ARMY PROVOST DSS — RESPONSE TEAM RESOURCE ALLOCATION BACKEND
# ======================================================================
#
# Academic B.Tech prototype.
#
# IMPORTANT:
# - Response-team information is synthetic.
# - Operational response categories originate from the existing DSS.
# - Team recommendations are deterministic decision-support outputs.
# - Final deployment authority remains with the human operator.
# ======================================================================

from pathlib import Path
from datetime import datetime
import uuid
import pandas as pd

from database import get_supabase_client



# ----------------------------------------------------------------------
# PROJECT PATHS
# ----------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

OUTPUTS_DIR = PROJECT_ROOT / "data"
LOGS_DIR = PROJECT_ROOT / "data"

RESPONSE_TEAM_REGISTRY_PATH = (
    OUTPUTS_DIR / "Response_Team_Registry.csv"
)

RESOURCE_ALLOCATION_AUDIT_PATH = (
    LOGS_DIR / "Response_Team_Allocation_Audit_Log.csv"
)


# ======================================================================
# DSS RESPONSE → CAPABILITY MAPPING
# ======================================================================

RESPONSE_CAPABILITY_MAPPING = {

    "Property / Asset Security Response": {
        "primary": "Property and Asset Security",
        "secondary": [
            "Incident Control",
            "Access and Perimeter Security"
        ]
    },

    "Personnel Safety / Provost Response": {
        "primary": "Personnel Safety",
        "secondary": [
            "Incident Control",
            "Medical Coordination"
        ]
    },

    "Administrative / Investigation Response": {
        "primary": "Investigation Support",
        "secondary": [
            "Incident Control"
        ]
    },

    "Controlled Substances / Security Response": {
        "primary": "Controlled Substances Response",
        "secondary": [
            "Incident Control",
            "Investigation Support"
        ]
    },

    "Vehicle / Mobility Security Response": {
        "primary": "Vehicle and Mobility Security",
        "secondary": [
            "Traffic and Movement Control",
            "Incident Control"
        ]
    },

    "Sensitive Incident / Specialized Response": {
        "primary": "Sensitive Incident Response",
        "secondary": [
            "Access and Perimeter Security",
            "Incident Control"
        ]
    }
}


# ======================================================================
# REGISTRY I/O
# ======================================================================


def load_response_team_registry(
    registry_path=None
):
    """
    Load the current synthetic response-team registry
    from Supabase.

    The registry_path parameter is retained only for
    compatibility with the existing function signature.
    """

    client = get_supabase_client()

    response = (
        client
        .table("response_teams")
        .select("*")
        .order("team_id")
        .execute()
    )

    records = response.data or []

    if not records:
        return pd.DataFrame()

    registry = pd.DataFrame(
        records
    )

    # Convert database column names to the existing
    # allocator's expected schema.
    registry = registry.rename(
        columns={
            "team_id":
                "Team_ID",

            "team_name":
                "Team_Name",

            "status":
                "Status",

            "current_zone":
                "Current_Zone",

            "primary_capability":
                "Primary_Capability",

            "secondary_capabilities":
                "Secondary_Capabilities",

            "readiness_level":
                "Readiness_Level",

            "personnel_strength":
                "Personnel_Strength",

            "vehicle_available":
                "Vehicle_Available",

            "capability_tags":
                "Capability_Tags",

            "current_assignment":
                "Current_Assignment",

            "last_updated":
                "Last_Updated"
        }
    )

    return registry



def save_response_team_registry(
    team_registry,
    registry_path=None
):
    """
    Persist the current synthetic response-team state
    to Supabase.

    Each Team_ID is upserted so assignments and releases
    survive Streamlit server restarts.
    """

    client = get_supabase_client()

    records = []

    for _, row in team_registry.iterrows():

        current_assignment = row.get(
            "Current_Assignment",
            None
        )

        if pd.isna(
            current_assignment
        ):
            current_assignment = None


        record = {
            "team_id":
                row["Team_ID"],

            "team_name":
                row["Team_Name"],

            "status":
                row["Status"],

            "current_zone":
                row["Current_Zone"],

            "primary_capability":
                row["Primary_Capability"],

            "secondary_capabilities":
                row["Secondary_Capabilities"],

            "readiness_level":
                row["Readiness_Level"],

            "personnel_strength":
                int(
                    row["Personnel_Strength"]
                ),

            "vehicle_available":
                bool(
                    row["Vehicle_Available"]
                ),

            "capability_tags":
                row["Capability_Tags"],

            "current_assignment":
                current_assignment
        }

        records.append(
            record
        )


    (
        client
        .table("response_teams")
        .upsert(
            records,
            on_conflict="team_id"
        )
        .execute()
    )

    return True


# ======================================================================
# CAPABILITY UTILITIES
# ======================================================================

def get_team_capabilities(team):
    """
    Return the complete capability set of one response team.
    """

    capabilities = {
        team["Primary_Capability"]
    }

    secondary = [
        cap.strip()
        for cap in str(
            team["Secondary_Capabilities"]
        ).split(";")
        if cap.strip()
    ]

    capabilities.update(secondary)

    return capabilities


def get_required_capabilities(
    operational_response
):
    """
    Translate an operational-response category from the existing DSS
    into the controlled capability vocabulary used by this allocator.
    """

    if (
        operational_response
        not in RESPONSE_CAPABILITY_MAPPING
    ):
        raise ValueError(
            "No resource capability mapping exists for "
            f"operational response: {operational_response}"
        )

    mapping = RESPONSE_CAPABILITY_MAPPING[
        operational_response
    ]

    return {
        "Primary_Required_Capability":
            mapping["primary"],

        "Secondary_Required_Capabilities":
            mapping["secondary"]
    }


# ======================================================================
# ELIGIBILITY FILTER
# ======================================================================

def filter_eligible_response_teams(
    team_registry,
    required_capability
):
    """
    Eligibility gates:

    1. Status must be AVAILABLE.
    2. Readiness must not be UNAVAILABLE.
    3. Team must possess the required primary capability
       either as a primary or secondary team capability.
    """

    eligible_records = []

    for _, team in team_registry.iterrows():

        capabilities = get_team_capabilities(
            team
        )

        is_available = (
            team["Status"] == "AVAILABLE"
        )

        readiness_ok = (
            team["Readiness_Level"]
            != "UNAVAILABLE"
        )

        capability_ok = (
            required_capability
            in capabilities
        )

        if (
            is_available
            and readiness_ok
            and capability_ok
        ):
            eligible_records.append(
                team.to_dict()
            )

    if not eligible_records:
        return pd.DataFrame(
            columns=team_registry.columns
        )

    return (
        pd.DataFrame(eligible_records)
        .reset_index(drop=True)
    )


# ======================================================================
# SUITABILITY SCORING
# ======================================================================

def personnel_strength_score(
    personnel_strength
):
    """
    Small supporting contribution to suitability score.
    """

    strength = int(
        personnel_strength
    )

    if strength >= 7:
        return 5
    elif strength == 6:
        return 4
    elif strength == 5:
        return 3
    elif strength == 4:
        return 2
    else:
        return 1


def score_response_team(
    team,
    required_capability,
    incident_zone
):
    """
    Calculate deterministic suitability score.

    Maximum score = 100.

    This is NOT a probability of success.
    """

    # --------------------------------------------------------------
    # Capability
    # --------------------------------------------------------------

    if (
        team["Primary_Capability"]
        == required_capability
    ):
        capability_score = 40
        capability_match = "PRIMARY"

    else:
        capability_score = 30
        capability_match = "SECONDARY"

    # --------------------------------------------------------------
    # Readiness
    # --------------------------------------------------------------

    if (
        team["Readiness_Level"]
        == "READY"
    ):
        readiness_score = 25

    elif (
        team["Readiness_Level"]
        == "LIMITED"
    ):
        readiness_score = 12

    else:
        readiness_score = 0

    # --------------------------------------------------------------
    # Zone
    # --------------------------------------------------------------

    if (
        team["Current_Zone"]
        == incident_zone
    ):
        zone_score = 20
        zone_relationship = "SAME ZONE"

    else:
        zone_score = 10
        zone_relationship = "DIFFERENT ZONE"

    # --------------------------------------------------------------
    # Vehicle
    # --------------------------------------------------------------

    vehicle_available = bool(
        team["Vehicle_Available"]
    )

    vehicle_score = (
        10 if vehicle_available else 0
    )

    # --------------------------------------------------------------
    # Personnel
    # --------------------------------------------------------------

    personnel_score = (
        personnel_strength_score(
            team["Personnel_Strength"]
        )
    )

    total_score = (
        capability_score
        + readiness_score
        + zone_score
        + vehicle_score
        + personnel_score
    )

    return {
        "Team_ID":
            team["Team_ID"],

        "Team_Name":
            team["Team_Name"],

        "Current_Zone":
            team["Current_Zone"],

        "Capability_Match":
            capability_match,

        "Readiness_Level":
            team["Readiness_Level"],

        "Zone_Relationship":
            zone_relationship,

        "Vehicle_Available":
            vehicle_available,

        "Personnel_Strength":
            int(team["Personnel_Strength"]),

        "Capability_Score":
            capability_score,

        "Readiness_Score":
            readiness_score,

        "Zone_Score":
            zone_score,

        "Vehicle_Score":
            vehicle_score,

        "Personnel_Score":
            personnel_score,

        "Suitability_Score":
            total_score
    }


def rank_eligible_response_teams(
    eligible_teams,
    required_capability,
    incident_zone
):
    """
    Rank eligible teams by deterministic suitability score.
    """

    ranking_records = []

    for _, team in eligible_teams.iterrows():

        ranking_records.append(
            score_response_team(
                team,
                required_capability,
                incident_zone
            )
        )

    if not ranking_records:
        return pd.DataFrame()

    ranking_df = pd.DataFrame(
        ranking_records
    )

    ranking_df = ranking_df.sort_values(
        by=[
            "Suitability_Score",
            "Team_ID"
        ],
        ascending=[
            False,
            True
        ]
    ).reset_index(drop=True)

    ranking_df.insert(
        0,
        "Rank",
        range(
            1,
            len(ranking_df) + 1
        )
    )

    return ranking_df


# ======================================================================
# MAIN RESOURCE ALLOCATION FUNCTION
# ======================================================================

def allocate_response_resource(
    operational_response,
    incident_zone,
    team_registry=None
):
    """
    Convert an existing DSS operational-response category into a
    ranked resource recommendation.

    Existing DSS
        ↓
    Operational Response
        ↓
    Required Capability
        ↓
    Availability / Readiness Filter
        ↓
    Suitability Ranking
        ↓
    Primary + Alternate Team
    """

    if team_registry is None:
        team_registry = (
            load_response_team_registry()
        )

    requirements = (
        get_required_capabilities(
            operational_response
        )
    )

    required_capability = requirements[
        "Primary_Required_Capability"
    ]

    eligible_teams = (
        filter_eligible_response_teams(
            team_registry,
            required_capability
        )
    )

    ranking = (
        rank_eligible_response_teams(
            eligible_teams,
            required_capability,
            incident_zone
        )
    )

    primary = None
    alternate = None

    if not ranking.empty:

        primary = (
            ranking.iloc[0]
            .to_dict()
        )

        if len(ranking) > 1:
            alternate = (
                ranking.iloc[1]
                .to_dict()
            )

    return {
        "Operational_Response":
            operational_response,

        "Required_Primary_Capability":
            required_capability,

        "Required_Secondary_Capabilities":
            requirements[
                "Secondary_Required_Capabilities"
            ],

        "Incident_Zone":
            incident_zone,

        "Eligible_Team_Count":
            len(eligible_teams),

        "Primary_Recommendation":
            primary,

        "Alternate_Recommendation":
            alternate,

        "Full_Ranking":
            ranking
    }


# ======================================================================
# TEAM STATE MANAGEMENT
# ======================================================================

def assign_response_team(
    team_registry,
    team_id,
    incident_id
):
    """
    Assign an AVAILABLE team.

    Returns a new registry DataFrame.
    """

    updated_registry = (
        team_registry.copy(deep=True)
    )

    team_match = updated_registry[
        updated_registry["Team_ID"]
        == team_id
    ]

    if team_match.empty:
        raise ValueError(
            f"Unknown Team ID: {team_id}"
        )

    team_index = (
        team_match.index[0]
    )

    status = updated_registry.loc[
        team_index,
        "Status"
    ]

    readiness = updated_registry.loc[
        team_index,
        "Readiness_Level"
    ]

    if status != "AVAILABLE":
        raise ValueError(
            f"{team_id} cannot be assigned. "
            f"Current status: {status}"
        )

    if readiness == "UNAVAILABLE":
        raise ValueError(
            f"{team_id} cannot be assigned. "
            "Readiness is UNAVAILABLE."
        )

    updated_registry.loc[
        team_index,
        "Status"
    ] = "ASSIGNED"

    updated_registry.loc[
        team_index,
        "Current_Assignment"
    ] = incident_id

    updated_registry.loc[
        team_index,
        "Last_Updated"
    ] = datetime.now()

    return updated_registry


def release_response_team(
    team_registry,
    team_id
):
    """
    Release an ASSIGNED team back to AVAILABLE state.
    """

    updated_registry = (
        team_registry.copy(deep=True)
    )

    team_match = updated_registry[
        updated_registry["Team_ID"]
        == team_id
    ]

    if team_match.empty:
        raise ValueError(
            f"Unknown Team ID: {team_id}"
        )

    team_index = (
        team_match.index[0]
    )

    status = updated_registry.loc[
        team_index,
        "Status"
    ]

    if status != "ASSIGNED":
        raise ValueError(
            f"{team_id} cannot be released. "
            f"Current status: {status}"
        )

    updated_registry.loc[
        team_index,
        "Status"
    ] = "AVAILABLE"

    updated_registry.loc[
        team_index,
        "Current_Assignment"
    ] = "None"

    updated_registry.loc[
        team_index,
        "Last_Updated"
    ] = datetime.now()

    return updated_registry


# ======================================================================
# HUMAN-IN-THE-LOOP DECISION
# ======================================================================

def process_operator_decision(
    allocation_result,
    team_registry,
    operator_uid,
    action,
    selected_team_id=None,
    override_reason=None,
    incident_id=None
):
    """
    Human operator either confirms the recommended team
    or overrides it with another eligible team.
    """

    action = str(
        action
    ).strip().upper()

    if action not in {
        "CONFIRM",
        "OVERRIDE"
    }:
        raise ValueError(
            "Action must be CONFIRM or OVERRIDE."
        )

    recommended = allocation_result[
        "Primary_Recommendation"
    ]

    if recommended is None:
        raise ValueError(
            "No deployable primary team exists."
        )

    recommended_team_id = (
        recommended["Team_ID"]
    )

    if action == "CONFIRM":

        final_team_id = (
            recommended_team_id
        )

        decision_type = "CONFIRMED"
        final_override_reason = None

    else:

        if not selected_team_id:
            raise ValueError(
                "selected_team_id is required "
                "for OVERRIDE."
            )

        if (
            selected_team_id
            == recommended_team_id
        ):
            raise ValueError(
                "Override team must differ from "
                "the recommended team."
            )

        ranking = allocation_result[
            "Full_Ranking"
        ]

        eligible_ids = set(
            ranking["Team_ID"]
            .tolist()
        )

        if (
            selected_team_id
            not in eligible_ids
        ):
            raise ValueError(
                f"{selected_team_id} is not "
                "currently eligible."
            )

        if (
            override_reason is None
            or not str(
                override_reason
            ).strip()
        ):
            raise ValueError(
                "Override reason is required."
            )

        final_team_id = (
            selected_team_id
        )

        decision_type = "OVERRIDDEN"

        final_override_reason = str(
            override_reason
        ).strip()

    if incident_id is None:
        incident_id = (
            "SIM-INC-"
            + datetime.now().strftime(
                "%Y%m%d%H%M%S"
            )
        )

    decision_id = (
        "DEC-"
        + uuid.uuid4().hex[
            :10
        ].upper()
    )

    updated_registry = (
        assign_response_team(
            team_registry,
            final_team_id,
            incident_id
        )
    )

    ranking = allocation_result[
        "Full_Ranking"
    ]

    selected_row = ranking[
        ranking["Team_ID"]
        == final_team_id
    ].iloc[0]

    decision_record = {

        "Decision_ID":
            decision_id,

        "Incident_ID":
            incident_id,

        "Timestamp":
            datetime.now(),

        "Operator_UID":
            operator_uid,

        "Operational_Response":
            allocation_result[
                "Operational_Response"
            ],

        "Incident_Zone":
            allocation_result[
                "Incident_Zone"
            ],

        "Required_Capability":
            allocation_result[
                "Required_Primary_Capability"
            ],

        "Recommended_Team_ID":
            recommended_team_id,

        "Recommended_Team_Score":
            recommended[
                "Suitability_Score"
            ],

        "Operator_Action":
            decision_type,

        "Selected_Team_ID":
            final_team_id,

        "Selected_Team_Score":
            selected_row[
                "Suitability_Score"
            ],

        "Override_Reason":
            final_override_reason
    }

    return (
        decision_record,
        updated_registry
    )


# ======================================================================
# AUDIT LOG
# ======================================================================



def append_resource_allocation_audit(
    decision_record,
    audit_path=None
):
    """
    Persist one human-approved resource-allocation decision
    to Supabase.

    NumPy / Pandas scalar values are converted to standard
    Python types before JSON serialization.
    """

    client = get_supabase_client()


    # --------------------------------------------------------
    # JSON-SAFE VALUE NORMALIZER
    # --------------------------------------------------------

    def json_safe(value):

        if value is None:
            return None

        # Pandas / NumPy missing values
        try:
            if pd.isna(value):
                return None
        except Exception:
            pass

        # NumPy scalar -> native Python scalar
        if hasattr(value, "item"):

            try:
                value = value.item()
            except Exception:
                pass

        # datetime / Timestamp -> ISO string
        if hasattr(value, "isoformat"):

            try:
                return value.isoformat()
            except Exception:
                pass

        # Explicitly normalize standard scalar types
        if isinstance(value, bool):
            return bool(value)

        if isinstance(value, int):
            return int(value)

        if isinstance(value, float):
            return float(value)

        if isinstance(value, str):
            return value

        return value


    record = {

        "decision_id":
            json_safe(
                decision_record.get(
                    "Decision_ID"
                )
            ),

        "incident_id":
            json_safe(
                decision_record.get(
                    "Incident_ID"
                )
            ),

        "decision_timestamp":
            json_safe(
                decision_record.get(
                    "Timestamp"
                )
            ),

        "operator_uid":
            json_safe(
                decision_record.get(
                    "Operator_UID"
                )
            ),

        "operational_response":
            json_safe(
                decision_record.get(
                    "Operational_Response"
                )
            ),

        "incident_zone":
            json_safe(
                decision_record.get(
                    "Incident_Zone"
                )
            ),

        "required_capability":
            json_safe(
                decision_record.get(
                    "Required_Capability"
                )
            ),

        "recommended_team_id":
            json_safe(
                decision_record.get(
                    "Recommended_Team_ID"
                )
            ),

        "recommended_team_score":
            json_safe(
                decision_record.get(
                    "Recommended_Team_Score"
                )
            ),

        "operator_action":
            json_safe(
                decision_record.get(
                    "Operator_Action"
                )
            ),

        "selected_team_id":
            json_safe(
                decision_record.get(
                    "Selected_Team_ID"
                )
            ),

        "selected_team_score":
            json_safe(
                decision_record.get(
                    "Selected_Team_Score"
                )
            ),

        "override_reason":
            json_safe(
                decision_record.get(
                    "Override_Reason"
                )
            )
    }


    (
        client
        .table(
            "resource_allocation_audit"
        )
        .upsert(
            record,
            on_conflict="decision_id"
        )
        .execute()
    )

    return True


# ======================================================================
# BACKEND INFORMATION
# ======================================================================

def backend_status():
    """
    Return simple backend metadata for diagnostics.
    """

    return {
        "Backend":
            "Army Provost Response Team Allocation",

        "Version":
            "1.0",

        "Team_Registry":
            str(
                RESPONSE_TEAM_REGISTRY_PATH
            ),

        "Audit_Log":
            str(
                RESOURCE_ALLOCATION_AUDIT_PATH
            ),

        "Operational_Response_Categories":
            len(
                RESPONSE_CAPABILITY_MAPPING
            ),

        "Human_In_The_Loop":
            True
    }
