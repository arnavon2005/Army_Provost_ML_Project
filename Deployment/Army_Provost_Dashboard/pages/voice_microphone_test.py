
import re
import tempfile
from datetime import datetime

import joblib
import pandas as pd
import streamlit as st
from faster_whisper import WhisperModel

from dashboard_utils import (
    execute_operational_analysis,
    execute_resource_allocation
)


# ==============================================================
# PAGE CONFIG
# ==============================================================

st.set_page_config(
    page_title="Voice Intake",
    page_icon="🎙️",
    layout="wide"
)

st.title("🎙️ Voice Helpline Intake")
st.caption(
    "Record an incident report, review the extracted details, "
    "and confirm them before DSS processing."
)


# ==============================================================
# PATHS
# ==============================================================

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

TAXONOMY_PATH = (
    BASE_DIR
    / "data"
    / "Army_Provost_Incident_Taxonomy.csv"
)

PREPROCESSOR_PATH = (
    BASE_DIR
    / "models"
    / "preprocessing_pipeline.pkl"
)


# ==============================================================
# LOAD DSS CATEGORIES
# ==============================================================

@st.cache_data
def load_incident_types():

    taxonomy_df = pd.read_csv(
        TAXONOMY_PATH
    )

    return (
        taxonomy_df["Primary Type"]
        .dropna()
        .astype(str)
        .drop_duplicates()
        .sort_values()
        .tolist()
    )


@st.cache_resource
def load_preprocessor():

    return joblib.load(
        PREPROCESSOR_PATH
    )


@st.cache_data
def load_location_categories():

    preprocessor = load_preprocessor()

    encoder = (
        preprocessor
        .named_transformers_["categorical"]
    )

    return list(
        encoder.categories_[1]
    )


incident_types = load_incident_types()
location_categories = load_location_categories()


# ==============================================================
# WHISPER MODEL
# ==============================================================

@st.cache_resource
def load_whisper_model():

    return WhisperModel(
        "tiny.en",
        device="cpu",
        compute_type="int8"
    )


# ==============================================================
# EXTRACTION MAPS
# ==============================================================

incident_keyword_map = {

    "BATTERY": [
        "fight",
        "fighting",
        "hit",
        "hitting",
        "beaten",
        "beating",
        "physical attack",
        "physical altercation"
    ],

    "ASSAULT": [
        "threatened to attack",
        "threatening to attack",
        "attempted attack",
        "attempt to attack"
    ],

    "THEFT": [
        "stolen",
        "stealing",
        "theft",
        "someone took",
        "missing property"
    ],

    "ROBBERY": [
        "robbery",
        "robbed",
        "mugged",
        "stolen at gunpoint",
        "stolen at knifepoint"
    ],

    "BURGLARY": [
        "burglary",
        "break in",
        "breaking into",
        "broke into",
        "forced entry"
    ],

    "MOTOR VEHICLE THEFT": [
        "vehicle stolen",
        "car stolen",
        "stolen car",
        "stolen vehicle"
    ],

    "CRIMINAL DAMAGE": [
        "damaged",
        "vandalised",
        "vandalized",
        "property damage",
        "destroyed property"
    ],

    "CRIMINAL TRESPASS": [
        "trespassing",
        "trespass",
        "unauthorized entry"
    ],

    "NARCOTICS": [
        "drugs",
        "narcotics",
        "illegal drugs",
        "drug possession"
    ],

    "WEAPONS VIOLATION": [
        "illegal weapon",
        "unauthorized weapon",
        "weapon violation",
        "carrying a weapon",
        "armed person"
    ],

    "HOMICIDE": [
        "killed",
        "murder",
        "murdered",
        "dead body",
        "fatal attack"
    ],

    "KIDNAPPING": [
        "kidnapped",
        "kidnapping",
        "abducted",
        "abduction"
    ],

    "INTIMIDATION": [
        "intimidating",
        "intimidation",
        "threatening",
        "threatened"
    ]
}


location_keyword_map = {

    "PARKING LOT": [
        "parking area",
        "parking lot",
        "car park"
    ],

    "STREET": [
        "street",
        "road",
        "roadway"
    ],

    "SIDEWALK": [
        "sidewalk",
        "footpath",
        "pavement"
    ],

    "RESIDENCE": [
        "residence",
        "home"
    ],

    "HOUSE": [
        "house"
    ],

    "APARTMENT": [
        "apartment",
        "flat"
    ],

    "GARAGE": [
        "garage"
    ],

    "RESTAURANT": [
        "restaurant"
    ],

    "BAR OR TAVERN": [
        "bar",
        "tavern",
        "pub"
    ],

    "HOSPITAL": [
        "hospital"
    ],

    "SCHOOL - PUBLIC BUILDING": [
        "school building",
        "inside the school"
    ],

    "COLLEGE / UNIVERSITY - GROUNDS": [
        "college campus",
        "university campus",
        "college grounds",
        "university grounds"
    ],

    "GOVERNMENT BUILDING / PROPERTY": [
        "government building",
        "government property"
    ]
}


# ==============================================================
# EXTRACTION FUNCTIONS
# ==============================================================

def match_from_keywords(
    text,
    mapping
):

    lowered = text.lower()

    matches = []

    for category, phrases in mapping.items():

        for phrase in phrases:

            if phrase.lower() in lowered:

                matches.append(
                    (
                        category,
                        phrase
                    )
                )

                break

    if not matches:
        return None, None

    matches.sort(
        key=lambda x: len(x[1]),
        reverse=True
    )

    return matches[0]


def detect_incident_type(text):

    lowered = text.lower()

    # Domestic violence
    domestic_relationship_terms = [
        "husband",
        "wife",
        "spouse",
        "boyfriend",
        "girlfriend",
        "partner",
        "family member"
    ]

    violence_terms = [
        "hit",
        "hitting",
        "beat",
        "beating",
        "beaten",
        "fight",
        "fighting",
        "attacked",
        "attack",
        "assaulted",
        "physical violence"
    ]

    relationship_found = next(
        (
            term
            for term in domestic_relationship_terms
            if term in lowered
        ),
        None
    )

    violence_found = next(
        (
            term
            for term in violence_terms
            if term in lowered
        ),
        None
    )

    if (
        relationship_found is not None
        and violence_found is not None
    ):
        return (
            "DOMESTIC VIOLENCE",
            f"{relationship_found} + {violence_found}"
        )

    # Motor vehicle theft
    vehicle_terms = [
        "car",
        "vehicle",
        "motorcycle",
        "motorbike",
        "bike",
        "scooter",
        "truck",
        "van",
        "automobile"
    ]

    vehicle_theft_terms = [
        "stolen",
        "stealing",
        "theft",
        "taken",
        "missing"
    ]

    vehicle_found = next(
        (
            term
            for term in vehicle_terms
            if term in lowered
        ),
        None
    )

    theft_found = next(
        (
            term
            for term in vehicle_theft_terms
            if term in lowered
        ),
        None
    )

    if (
        vehicle_found is not None
        and theft_found is not None
    ):
        return (
            "MOTOR VEHICLE THEFT",
            f"{vehicle_found} + {theft_found}"
        )

    # Robbery
    for term in [
        "robbery",
        "robbed",
        "mugged",
        "at gunpoint",
        "at knifepoint"
    ]:

        if term in lowered:
            return (
                "ROBBERY",
                term
            )

    # Burglary
    for term in [
        "broke into",
        "breaking into",
        "break in",
        "forced entry",
        "burglary"
    ]:

        if term in lowered:
            return (
                "BURGLARY",
                term
            )

    return match_from_keywords(
        text,
        incident_keyword_map
    )


def extract_incident_information(
    transcript
):

    text = transcript.strip()

    incident_type, incident_phrase = (
        detect_incident_type(
            text
        )
    )

    location_description, location_phrase = (
        match_from_keywords(
            text,
            location_keyword_map
        )
    )

    lowered = text.lower()

    domestic = None

    domestic_terms = [
        "husband",
        "wife",
        "spouse",
        "boyfriend",
        "girlfriend",
        "domestic",
        "family member",
        "partner"
    ]

    if any(
        term in lowered
        for term in domestic_terms
    ):
        domestic = True

    incident_zone = None

    zone_match = re.search(
        r"\bzone\s+([a-h])\b",
        lowered
    )

    if zone_match:

        incident_zone = (
            "Zone "
            + zone_match.group(1).upper()
        )

    injury_terms = [
        "injured",
        "hurt",
        "wounded",
        "bleeding"
    ]

    injury_mentioned = any(
        term in lowered
        for term in injury_terms
    )

    return {

        "Incident Type":
            incident_type,

        "Incident Match Phrase":
            incident_phrase,

        "Location Description":
            location_description,

        "Location Match Phrase":
            location_phrase,

        "Domestic Incident":
            domestic,

        "Incident Zone":
            incident_zone,

        "Injury Mentioned":
            injury_mentioned
    }


# ==============================================================
# MICROPHONE
# ==============================================================

st.subheader("1. Record Incident Report")

audio_value = st.audio_input(
    "Record caller report"
)


if audio_value is not None:

    st.audio(
        audio_value,
        format="audio/wav"
    )

    if st.button(
        "Transcribe Incident",
        type="primary"
    ):

        with st.spinner(
            "Transcribing audio..."
        ):

            audio_bytes = (
                audio_value.getvalue()
            )

            with tempfile.NamedTemporaryFile(
                suffix=".wav",
                delete=False
            ) as temp_audio:

                temp_audio.write(
                    audio_bytes
                )

                temp_audio_path = (
                    temp_audio.name
                )

            whisper_model = (
                load_whisper_model()
            )

            segments, _ = (
                whisper_model.transcribe(
                    temp_audio_path,
                    beam_size=5,
                    language="en"
                )
            )

            transcript = " ".join(
                segment.text.strip()
                for segment in segments
            ).strip()

            extraction = (
                extract_incident_information(
                    transcript
                )
            )

            st.session_state[
                "voice_transcript"
            ] = transcript

            st.session_state[
                "voice_extraction"
            ] = extraction


# ==============================================================
# TRANSCRIPT
# ==============================================================

if "voice_transcript" in st.session_state:

    st.divider()

    st.subheader(
        "2. Transcript"
    )

    transcript = st.text_area(
        "Review transcript",
        value=st.session_state[
            "voice_transcript"
        ],
        height=110
    )

    st.session_state[
        "voice_transcript"
    ] = transcript


# ==============================================================
# OPERATOR REVIEW
# ==============================================================

if "voice_extraction" in st.session_state:

    extraction = (
        st.session_state[
            "voice_extraction"
        ]
    )

    st.divider()

    st.subheader(
        "3. Operator Verification"
    )

    st.info(
        "AI-generated fields are suggestions only. "
        "The operator must review and confirm them."
    )

    left, right = st.columns(2)

    with left:

        suggested_incident = (
            extraction["Incident Type"]
        )

        incident_index = (
            incident_types.index(
                suggested_incident
            )
            if suggested_incident
            in incident_types
            else 0
        )

        confirmed_incident = (
            st.selectbox(
                "Incident Type",
                options=incident_types,
                index=incident_index
            )
        )

        suggested_location = (
            extraction[
                "Location Description"
            ]
        )

        location_index = (
            location_categories.index(
                suggested_location
            )
            if suggested_location
            in location_categories
            else 0
        )

        confirmed_location = (
            st.selectbox(
                "Location Description",
                options=location_categories,
                index=location_index
            )
        )

        domestic_default = (
            extraction[
                "Domestic Incident"
            ]
        )

        domestic_options = [
            "Select...",
            "No",
            "Yes"
        ]

        if domestic_default is True:
            domestic_index = 2
        elif domestic_default is False:
            domestic_index = 1
        else:
            domestic_index = 0

        confirmed_domestic = (
            st.selectbox(
                "Domestic Incident",
                options=domestic_options,
                index=domestic_index
            )
        )

        zone_options = [
            "Select...",
            "Zone A",
            "Zone B",
            "Zone C",
            "Zone D",
            "Zone E",
            "Zone F",
            "Zone G",
            "Zone H"
        ]

        suggested_zone = (
            extraction[
                "Incident Zone"
            ]
        )

        zone_index = (
            zone_options.index(
                suggested_zone
            )
            if suggested_zone
            in zone_options
            else 0
        )

        confirmed_zone = (
            st.selectbox(
                "Incident Zone",
                options=zone_options,
                index=zone_index
            )
        )


    with right:

        now = datetime.now()

        year = st.number_input(
            "Year",
            value=now.year,
            step=1
        )

        month = st.number_input(
            "Month",
            min_value=1,
            max_value=12,
            value=now.month,
            step=1
        )

        day = st.number_input(
            "Day",
            min_value=1,
            max_value=31,
            value=now.day,
            step=1
        )

        hour = st.number_input(
            "Hour",
            min_value=0,
            max_value=23,
            value=now.hour,
            step=1
        )

        district = st.number_input(
            "District",
            min_value=0,
            value=0,
            step=1
        )

        beat = st.number_input(
            "Beat",
            min_value=0,
            value=0,
            step=1
        )

        ward = st.number_input(
            "Ward",
            min_value=0,
            value=0,
            step=1
        )

        community_area = (
            st.number_input(
                "Community Area",
                min_value=0,
                value=0,
                step=1
            )
        )


    st.divider()

    st.subheader(
        "4. Extracted Safety Signals"
    )

    st.write(
        "Injury mentioned:",
        (
            "Yes"
            if extraction[
                "Injury Mentioned"
            ]
            else "No"
        )
    )


    # ==========================================================
    # VALIDATION
    # ==========================================================

    unresolved = []

    if confirmed_domestic == "Select...":
        unresolved.append(
            "Domestic Incident"
        )

    if confirmed_zone == "Select...":
        unresolved.append(
            "Incident Zone"
        )

    if district == 0:
        unresolved.append(
            "District"
        )

    if beat == 0:
        unresolved.append(
            "Beat"
        )

    if ward == 0:
        unresolved.append(
            "Ward"
        )

    if community_area == 0:
        unresolved.append(
            "Community Area"
        )


    if unresolved:

        st.warning(
            "Operator confirmation required for: "
            + ", ".join(unresolved)
        )

    else:

        st.success(
            "All required fields have been confirmed."
        )


    # ==========================================================
    # PREPARE CONFIRMED RECORD
    # ==============================================================

    if st.button(
        "Confirm Voice Intake"
    ):

        if unresolved:

            st.error(
                "Complete all required fields "
                "before confirming."
            )

        else:

            confirmed_record = {

                "primary_type":
                    confirmed_incident,

                "location_description":
                    confirmed_location,

                "domestic":
                    (
                        confirmed_domestic
                        == "Yes"
                    ),

                "incident_zone":
                    confirmed_zone,

                "year":
                    int(year),

                "month":
                    int(month),

                "day":
                    int(day),

                "hour":
                    int(hour),

                "district":
                    int(district),

                "beat":
                    int(beat),

                "ward":
                    int(ward),

                "community_area":
                    int(
                        community_area
                    ),

                "transcript":
                    transcript,

                "injury_mentioned":
                    extraction[
                        "Injury Mentioned"
                    ]
            }

            st.session_state[
                "confirmed_voice_record"
            ] = confirmed_record

            st.success(
                "Voice intake confirmed. "
                "Record is ready for DSS integration."
            )

            st.json(
                confirmed_record
            )


# ==============================================================
# DSS EXECUTION — HUMAN CONFIRMATION REQUIRED
# ==============================================================

if "confirmed_voice_record" in st.session_state:

    st.divider()

    st.subheader(
        "5. Decision Support Analysis"
    )

    st.warning(
        "The incident has been confirmed by the operator, "
        "but has not yet been processed by the DSS."
    )

    if st.button(
        "Run Confirmed Intake Through DSS",
        type="primary"
    ):

        confirmed = (
            st.session_state[
                "confirmed_voice_record"
            ]
        )

        try:

            # --------------------------------------------------
            # EXISTING ML + DSS PATH
            # --------------------------------------------------

            analysis = (
                execute_operational_analysis(
                    primary_type=
                        confirmed["primary_type"],

                    location_description=
                        confirmed[
                            "location_description"
                        ],

                    domestic=
                        confirmed["domestic"],

                    year=
                        confirmed["year"],

                    month=
                        confirmed["month"],

                    day=
                        confirmed["day"],

                    hour=
                        confirmed["hour"],

                    district=
                        confirmed["district"],

                    beat=
                        confirmed["beat"],

                    ward=
                        confirmed["ward"],

                    community_area=
                        confirmed[
                            "community_area"
                        ],

                    incident_zone=
                        confirmed[
                            "incident_zone"
                        ]
                )
            )

            decision = analysis[
                "Decision"
            ]

            # --------------------------------------------------
            # EXISTING RESOURCE ALLOCATION PATH
            # --------------------------------------------------

            resource_result = (
                execute_resource_allocation(
                    operational_response=
                        decision[
                            "Recommended Response Type"
                        ],

                    incident_zone=
                        confirmed[
                            "incident_zone"
                        ]
                )
            )

            allocation = resource_result[
                "Allocation Result"
            ]

            # Preserve results across Streamlit reruns
            st.session_state[
                "voice_dss_analysis"
            ] = analysis

            st.session_state[
                "voice_resource_result"
            ] = resource_result

            st.success(
                "Confirmed voice intake processed "
                "successfully."
            )

        except Exception as exc:

            st.error(
                "Voice intake could not be processed "
                "by the DSS."
            )

            st.exception(
                exc
            )


# ==============================================================
# DISPLAY DSS RESULT
# ==============================================================

if "voice_dss_analysis" in st.session_state:

    analysis = (
        st.session_state[
            "voice_dss_analysis"
        ]
    )

    decision = analysis[
        "Decision"
    ]

    st.markdown(
        "### DSS Recommendation"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Priority",
            decision.get(
                "Priority",
                "N/A"
            )
        )

    with col2:

        st.metric(
            "Recommended Response",
            decision.get(
                "Recommended Response Type",
                "N/A"
            )
        )

    with col3:

        arrest_probability = (
            decision.get(
                "Arrest Probability"
            )
        )

        if arrest_probability is None:

            probability_display = "N/A"

        else:

            try:

                probability_value = float(
                    arrest_probability
                )

                if probability_value <= 1:
                    probability_value *= 100

                probability_display = (
                    f"{probability_value:.2f}%"
                )

            except Exception:

                probability_display = str(
                    arrest_probability
                )

        st.metric(
            "Arrest Probability",
            probability_display
        )


# ==============================================================
# DISPLAY RESOURCE RECOMMENDATION
# ==============================================================

if "voice_resource_result" in st.session_state:

    resource_result = (
        st.session_state[
            "voice_resource_result"
        ]
    )

    allocation = resource_result[
        "Allocation Result"
    ]

    st.markdown(
        "### Response Resource Recommendation"
    )

    primary_team = allocation.get(
        "Primary_Recommendation"
    )

    alternate_team = allocation.get(
        "Alternate_Recommendation"
    )

    if primary_team is None:

        st.warning(
            "No eligible response team is currently "
            "available for the recommended capability."
        )

    else:

        st.write(
            "**Primary Recommended Team:**",
            primary_team.get(
                "Team_Name",
                primary_team.get(
                    "Team_ID",
                    "N/A"
                )
            )
        )

    if alternate_team is not None:

        st.write(
            "**Alternate Team:**",
            alternate_team.get(
                "Team_Name",
                alternate_team.get(
                    "Team_ID",
                    "N/A"
                )
            )
        )
