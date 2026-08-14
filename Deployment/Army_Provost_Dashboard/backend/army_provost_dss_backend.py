from pathlib import Path

# ============================================================
# ARMY PROVOST DECISION SUPPORT SYSTEM
# PERSISTENT BACKEND MODULE
# ============================================================

import os
import pandas as pd
import joblib
from datetime import datetime


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = (
    str(Path(__file__).resolve().parents[1])
)

MODELS_PATH = os.path.join(
    PROJECT_ROOT,
    "models"
)

OUTPUTS_PATH = os.path.join(
    PROJECT_ROOT,
    "data"
)


# ============================================================
# EXISTING MODEL ARTIFACTS
# ============================================================

RF_MODEL_PATH = os.path.join(
    MODELS_PATH,
    "final_random_forest.pkl"
)

PREPROCESSOR_PATH = os.path.join(
    MODELS_PATH,
    "preprocessing_pipeline.pkl"
)

TAXONOMY_PATH = os.path.join(
    OUTPUTS_PATH,
    "Army_Provost_Incident_Taxonomy.csv"
)

RESPONSE_MAPPING_PATH = os.path.join(
    OUTPUTS_PATH,
    "Army_Provost_Operational_Response_Mapping.csv"
)


# ============================================================
# LOAD EXISTING ARTIFACTS
# ============================================================

rf_model = joblib.load(
    RF_MODEL_PATH
)

preprocessing_pipeline = joblib.load(
    PREPROCESSOR_PATH
)

taxonomy_df = pd.read_csv(
    TAXONOMY_PATH
)

response_mapping_df = pd.read_csv(
    RESPONSE_MAPPING_PATH
)


# ============================================================
# TAXONOMY LOOKUP
# ============================================================

taxonomy_lookup = (
    taxonomy_df
    .set_index("Primary Type")
    .to_dict("index")
)


# ============================================================
# RESPONSE LOOKUP
# ============================================================

response_lookup = (
    response_mapping_df
    .set_index("Primary Type")
    .to_dict("index")
)


# ============================================================
# INCIDENT CLASSIFICATION
# ============================================================

def classify_army_provost_incident(primary_type):

    primary_type = (
        str(primary_type)
        .strip()
        .upper()
    )

    if primary_type not in taxonomy_lookup:
        raise ValueError(
            f"'{primary_type}' is not present in "
            "the Army Provost incident taxonomy."
        )

    taxonomy_entry = taxonomy_lookup[
        primary_type
    ]

    response_entry = response_lookup[
        primary_type
    ]

    return {
        "Primary Type":
            primary_type,

        "Provost Incident Category":
            taxonomy_entry[
                "Provost Incident Category"
            ],

        "Incident Subcategory":
            taxonomy_entry[
                "Incident Subcategory"
            ],

        "Priority Relevance":
            taxonomy_entry[
                "Priority Relevance"
            ],

        "Mapping Rationale":
            taxonomy_entry[
                "Mapping Rationale"
            ],

        "Recommended Response Type":
            response_entry[
                "Recommended Response Type"
            ]
    }


# ============================================================
# RANDOM FOREST PREDICTION
# ============================================================

def predict_arrest_probability(
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

    input_data = pd.DataFrame([
        {
            "Primary Type": primary_type,
            "Location Description":
                location_description,
            "Domestic": domestic,
            "Year": year,
            "Month": month,
            "Day": day,
            "Hour": hour,
            "District": district,
            "Beat": beat,
            "Ward": ward,
            "Community Area": community_area
        }
    ])

    processed_input = (
        preprocessing_pipeline.transform(
            input_data
        )
    )

    probabilities = (
        rf_model.predict_proba(
            processed_input
        )
    )

    arrest_probability = float(
        probabilities[0][1]
    )

    threshold = 0.50

    arrest_prediction = (
        "Likely Arrest"
        if arrest_probability >= threshold
        else "Less Likely Arrest"
    )

    return {
        "Arrest Probability":
            arrest_probability,

        "Arrest Probability (%)":
            round(
                arrest_probability * 100,
                2
            ),

        "Arrest Prediction":
            arrest_prediction,

        "Decision Threshold":
            threshold
    }


# ============================================================
# INTEGRATED DECISION ENGINE
# ============================================================

def army_provost_decision_engine(
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

    classification = (
        classify_army_provost_incident(
            primary_type
        )
    )

    ml_result = (
        predict_arrest_probability(
            primary_type=primary_type,
            location_description=
                location_description,
            domestic=domestic,
            year=year,
            month=month,
            day=day,
            hour=hour,
            district=district,
            beat=beat,
            ward=ward,
            community_area=
                community_area
        )
    )

    return {
        "Primary Type":
            classification["Primary Type"],

        "Location Description":
            location_description,

        "Domestic":
            domestic,

        "Provost Incident Category":
            classification[
                "Provost Incident Category"
            ],

        "Incident Subcategory":
            classification[
                "Incident Subcategory"
            ],

        "Priority":
            classification[
                "Priority Relevance"
            ],

        "Arrest Probability":
            ml_result[
                "Arrest Probability"
            ],

        "Arrest Probability (%)":
            ml_result[
                "Arrest Probability (%)"
            ],

        "Arrest Prediction":
            ml_result[
                "Arrest Prediction"
            ],

        "Recommended Response Type":
            classification[
                "Recommended Response Type"
            ],

        "Year": year,
        "Month": month,
        "Day": day,
        "Hour": hour,
        "District": district,
        "Beat": beat,
        "Ward": ward,
        "Community Area":
            community_area
    }


# ============================================================
# INPUT VALIDATION
# ============================================================

def validate_dss_input(
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

    if (
        primary_type is None
        or str(primary_type).strip() == ""
    ):
        raise ValueError(
            "Primary Type is required."
        )

    if (
        location_description is None
        or str(location_description).strip() == ""
    ):
        raise ValueError(
            "Location Description is required."
        )

    primary_type = (
        str(primary_type)
        .strip()
        .upper()
    )

    location_description = (
        str(location_description)
        .strip()
        .upper()
    )

    if isinstance(domestic, str):

        domestic_normalized = (
            domestic.strip().lower()
        )

        if domestic_normalized in [
            "true", "yes", "1"
        ]:
            domestic = True

        elif domestic_normalized in [
            "false", "no", "0"
        ]:
            domestic = False

        else:
            raise ValueError(
                "Domestic must be True/False."
            )

    else:
        domestic = bool(domestic)

    numeric_values = {
        "Year": year,
        "Month": month,
        "Day": day,
        "Hour": hour,
        "District": district,
        "Beat": beat,
        "Ward": ward,
        "Community Area":
            community_area
    }

    normalized_numeric = {}

    for field, value in numeric_values.items():

        if value is None:
            raise ValueError(
                f"{field} is required."
            )

        try:
            normalized_numeric[field] = int(
                value
            )

        except (ValueError, TypeError):

            raise ValueError(
                f"{field} must be numeric."
            )

    if not 1 <= normalized_numeric["Month"] <= 12:
        raise ValueError(
            "Month must be between 1 and 12."
        )

    if not 1 <= normalized_numeric["Day"] <= 31:
        raise ValueError(
            "Day must be between 1 and 31."
        )

    if not 0 <= normalized_numeric["Hour"] <= 23:
        raise ValueError(
            "Hour must be between 0 and 23."
        )

    if primary_type not in taxonomy_lookup:
        raise ValueError(
            f"'{primary_type}' is not present in "
            "the Army Provost incident taxonomy."
        )

    return {
        "primary_type":
            primary_type,

        "location_description":
            location_description,

        "domestic":
            domestic,

        "year":
            normalized_numeric["Year"],

        "month":
            normalized_numeric["Month"],

        "day":
            normalized_numeric["Day"],

        "hour":
            normalized_numeric["Hour"],

        "district":
            normalized_numeric["District"],

        "beat":
            normalized_numeric["Beat"],

        "ward":
            normalized_numeric["Ward"],

        "community_area":
            normalized_numeric[
                "Community Area"
            ]
    }


# ============================================================
# STANDARDIZED DECISION RECORD
# ============================================================

def create_decision_record(
    decision_result
):

    decision_id = (
        "AP-DSS-"
        + datetime.now().strftime(
            "%Y%m%d-%H%M%S-%f"
        )
    )

    decision_timestamp = (
        datetime.now().isoformat(
            timespec="seconds"
        )
    )

    return {
        "Decision ID":
            decision_id,

        "Decision Timestamp":
            decision_timestamp,

        "Primary Type":
            decision_result["Primary Type"],

        "Location Description":
            decision_result[
                "Location Description"
            ],

        "Domestic":
            decision_result["Domestic"],

        "Provost Incident Category":
            decision_result[
                "Provost Incident Category"
            ],

        "Incident Subcategory":
            decision_result[
                "Incident Subcategory"
            ],

        "Priority":
            decision_result["Priority"],

        "Arrest Probability":
            decision_result[
                "Arrest Probability"
            ],

        "Arrest Probability (%)":
            decision_result[
                "Arrest Probability (%)"
            ],

        "Arrest Prediction":
            decision_result[
                "Arrest Prediction"
            ],

        "Recommended Response Type":
            decision_result[
                "Recommended Response Type"
            ],

        "Year":
            decision_result["Year"],

        "Month":
            decision_result["Month"],

        "Day":
            decision_result["Day"],

        "Hour":
            decision_result["Hour"],

        "District":
            decision_result["District"],

        "Beat":
            decision_result["Beat"],

        "Ward":
            decision_result["Ward"],

        "Community Area":
            decision_result["Community Area"]
    }


# ============================================================
# DECISION INTERPRETATION
# ============================================================

def interpret_decision_record(
    decision_record
):

    priority = decision_record[
        "Priority"
    ]

    arrest_probability = decision_record[
        "Arrest Probability (%)"
    ]

    arrest_prediction = decision_record[
        "Arrest Prediction"
    ]

    return {
        "Priority Interpretation":
            f"Official incident priority is "
            f"{priority}.",

        "ML Interpretation":
            f"The Random Forest estimates an "
            f"arrest probability of "
            f"{arrest_probability:.2f}% and "
            f"classifies the incident as "
            f"'{arrest_prediction}'.",

        "Signal Relationship":
            "Priority and ML arrest probability "
            "are separate decision-support "
            "indicators. The ML result does not "
            "override the established incident "
            "priority.",

        "Response Interpretation":
            f"The mapped response pathway is "
            f"'{decision_record['Recommended Response Type']}'. "
            "This is a recommendation for operator "
            "consideration, not an autonomous "
            "deployment decision."
    }


# ============================================================
# OPERATOR SUMMARY
# ============================================================

def generate_operator_summary(
    decision_result
):

    return (
        f"INCIDENT: "
        f"{decision_result['Primary Type']}\n"
        f"LOCATION: "
        f"{decision_result['Location Description']}\n"
        f"DOMESTIC: "
        f"{decision_result['Domestic']}\n\n"

        f"PROVOST CATEGORY: "
        f"{decision_result['Provost Incident Category']}\n"

        f"INCIDENT SUBCATEGORY: "
        f"{decision_result['Incident Subcategory']}\n"

        f"PRIORITY: "
        f"{decision_result['Priority']}\n\n"

        f"ML ARREST PROBABILITY: "
        f"{decision_result['Arrest Probability (%)']:.2f}%\n"

        f"ML ASSESSMENT: "
        f"{decision_result['Arrest Prediction']}\n\n"

        f"RECOMMENDED RESPONSE PATHWAY: "
        f"{decision_result['Recommended Response Type']}\n\n"

        f"OPERATOR NOTE: "
        "This output is a decision-support "
        "recommendation. Final operational "
        "decisions remain with the authorized "
        "operator."
    )


# ============================================================
# COMPLETE DSS ENTRY POINT
# ============================================================

def run_army_provost_dss(
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

    decision_result = (
        army_provost_decision_engine(
            primary_type=primary_type,
            location_description=
                location_description,
            domestic=domestic,
            year=year,
            month=month,
            day=day,
            hour=hour,
            district=district,
            beat=beat,
            ward=ward,
            community_area=
                community_area
        )
    )

    decision_record = (
        create_decision_record(
            decision_result
        )
    )

    interpretation = (
        interpret_decision_record(
            decision_record
        )
    )

    operator_summary = (
        generate_operator_summary(
            decision_result
        )
    )

    return {
        "Decision":
            decision_result,

        "Decision Record":
            decision_record,

        "Interpretation":
            interpretation,

        "Operator Summary":
            operator_summary
    }


# ============================================================
# DASHBOARD EXECUTION ENTRY POINT
# ============================================================

def execute_dashboard_dss(
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

    validated_input = (
        validate_dss_input(
            primary_type=primary_type,
            location_description=
                location_description,
            domestic=domestic,
            year=year,
            month=month,
            day=day,
            hour=hour,
            district=district,
            beat=beat,
            ward=ward,
            community_area=
                community_area
        )
    )

    dss_result = (
        run_army_provost_dss(
            **validated_input
        )
    )

    return {
        "Validated Input":
            validated_input,

        "DSS Result":
            dss_result
    }


# ============================================================
# BACKEND STATUS
# ============================================================

BACKEND_STATUS = {
    "Random Forest": os.path.exists(
        RF_MODEL_PATH
    ),

    "Preprocessing Pipeline":
        os.path.exists(
            PREPROCESSOR_PATH
        ),

    "Incident Taxonomy":
        os.path.exists(
            TAXONOMY_PATH
        ),

    "Response Mapping":
        os.path.exists(
            RESPONSE_MAPPING_PATH
        )
}



# === ARMY PROVOST STRUCTURED RESPONSE GUIDANCE EXTENSION ===

# ------------------------------------------------------------
# Structured response guidance
#
# Engineering prototype decision-support guidance only.
# This is not represented as official Indian Army SOP.
# ------------------------------------------------------------

RESPONSE_GUIDANCE_PATH = os.path.join(
    OUTPUTS_PATH,
    "Army_Provost_Response_Guidance.csv"
)


if not os.path.exists(RESPONSE_GUIDANCE_PATH):

    raise FileNotFoundError(
        "Structured response guidance file not found: "
        f"{RESPONSE_GUIDANCE_PATH}"
    )


response_guidance_df = pd.read_csv(
    RESPONSE_GUIDANCE_PATH
)


required_guidance_columns = [
    "Recommended Response Type",
    "Immediate Operator Guidance",
    "Coordination / Notification",
    "Scene / Evidence Considerations",
    "Escalation / Follow-up"
]


missing_guidance_columns = [
    column
    for column in required_guidance_columns
    if column not in response_guidance_df.columns
]


if missing_guidance_columns:

    raise ValueError(
        "Structured response guidance is missing "
        f"required columns: {missing_guidance_columns}"
    )


response_guidance_lookup = (
    response_guidance_df
    .set_index(
        "Recommended Response Type"
    )
    [
        [
            "Immediate Operator Guidance",
            "Coordination / Notification",
            "Scene / Evidence Considerations",
            "Escalation / Follow-up"
        ]
    ]
    .to_dict(
        orient="index"
    )
)


# ------------------------------------------------------------
# Preserve validated dashboard-facing DSS function
# ------------------------------------------------------------

_execute_dashboard_dss_without_guidance = (
    execute_dashboard_dss
)


# ------------------------------------------------------------
# Extended dashboard-facing DSS function
# ------------------------------------------------------------

def execute_dashboard_dss(
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

    result = (
        _execute_dashboard_dss_without_guidance(
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
    )


    dss_result = result[
        "DSS Result"
    ]


    decision = dss_result[
        "Decision"
    ]


    response_type = (
        decision[
            "Recommended Response Type"
        ]
    )


    guidance = (
        response_guidance_lookup.get(
            response_type
        )
    )


    if guidance is None:

        raise KeyError(
            "No structured response guidance found for "
            f"response type: {response_type}"
        )


    # --------------------------------------------------------
    # Add structured operator guidance without changing
    # existing validated DSS fields
    # --------------------------------------------------------

    dss_result[
        "Response Guidance"
    ] = {

        "Recommended Response Type":
            response_type,

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
            "Prototype Decision-Support Guidance"
    }


    return result


# === END STRUCTURED RESPONSE GUIDANCE EXTENSION ===

