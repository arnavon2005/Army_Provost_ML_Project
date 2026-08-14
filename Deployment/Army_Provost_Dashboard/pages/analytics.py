
import os

import pandas as pd
import streamlit as st

from dashboard_utils import (
    PROJECT_ROOT
)


# ============================================================
# FIXED ANALYTICS PATHS
# ============================================================

OUTPUTS_PATH = os.path.join(
    PROJECT_ROOT,
    "Outputs"
)

FIGURES_PATH = os.path.join(
    PROJECT_ROOT,
    "Figures"
)

MODEL_COMPARISON_PATH = os.path.join(
    OUTPUTS_PATH,
    "Final_Model_Performance_Comparison.csv"
)

FEATURE_IMPORTANCE_PATH = os.path.join(
    OUTPUTS_PATH,
    "Random_Forest_Aggregated_Feature_Importance.csv"
)

MODEL_COMPARISON_FIGURE = os.path.join(
    FIGURES_PATH,
    "Model_Performance_Comparison.png"
)

FEATURE_IMPORTANCE_FIGURE = os.path.join(
    FIGURES_PATH,
    "Random_Forest_Aggregated_Feature_Importance.png"
)


# ============================================================
# PAGE HEADER
# ============================================================

st.title(
    "📊 Analytics"
)

st.caption(
    "Machine Learning & Technical Assessment"
)

st.info(
    "This page contains technical Machine Learning information "
    "for analytical review. These metrics do not determine "
    "incident priority or replace operational judgment."
)


# ============================================================
# MODEL OVERVIEW
# ============================================================

st.subheader(
    "01 · Deployed Model"
)

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Model",
        "Random Forest"
    )


with col2:

    st.metric(
        "Prediction Target",
        "Arrest"
    )


with col3:

    st.metric(
        "Decision Threshold",
        "0.50"
    )


with col4:

    st.metric(
        "Encoded Features",
        "231"
    )


st.markdown(
    """
The deployed Random Forest estimates the **historical likelihood that an
arrest was recorded for incidents with similar characteristics**.

It does **not** estimate:

- incident severity,
- threat level,
- guilt,
- legal outcome,
- or required operational response.

Operational priority is determined separately by the deterministic
Army Provost-oriented taxonomy.
"""
)


st.divider()


# ============================================================
# MODEL PERFORMANCE
# ============================================================

st.subheader(
    "02 · Model Performance Comparison"
)


if os.path.exists(
    MODEL_COMPARISON_PATH
):

    comparison_df = pd.read_csv(
        MODEL_COMPARISON_PATH
    )

    st.dataframe(
        comparison_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.warning(
        "Model performance comparison CSV was not found."
    )


if os.path.exists(
    MODEL_COMPARISON_FIGURE
):

    st.image(
        MODEL_COMPARISON_FIGURE,
        caption="Model Performance Comparison",
        use_container_width=True
    )


with st.expander(
    "Why was Random Forest selected?"
):

    st.markdown(
        """
CatBoost achieved the highest overall Accuracy, Precision, F1 Score,
and ROC-AUC among the tested models.

However, the deployed baseline Random Forest was retained for Version 1.0
after considering:

- positive-class recall,
- balanced overall performance,
- existing validated preprocessing and inference architecture,
- computational limitations of the CPU-only Colab environment,
- and system integration stability.

The deployed Random Forest therefore represents an **engineering trade-off**,
not a claim that it is universally superior to every tested model.
"""
    )


st.divider()


# ============================================================
# FEATURE IMPORTANCE
# ============================================================

st.subheader(
    "03 · Random Forest Feature Importance"
)


if os.path.exists(
    FEATURE_IMPORTANCE_PATH
):

    importance_df = pd.read_csv(
        FEATURE_IMPORTANCE_PATH
    )

    st.dataframe(
        importance_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.warning(
        "Aggregated feature-importance CSV was not found."
    )


if os.path.exists(
    FEATURE_IMPORTANCE_FIGURE
):

    st.image(
        FEATURE_IMPORTANCE_FIGURE,
        caption=(
            "Random Forest Aggregated Feature Importance"
        ),
        use_container_width=True
    )


st.caption(
    "Feature importance describes how strongly the trained model "
    "uses available features for prediction. It should not be "
    "interpreted as evidence of causation."
)


st.divider()


# ============================================================
# ML INTERPRETATION
# ============================================================

st.subheader(
    "04 · Interpreting ML Output"
)


col1, col2 = st.columns(2)


with col1:

    with st.container(
        border=True
    ):

        st.markdown(
            "### Likely Arrest"
        )

        st.write(
            "Arrest probability is greater than or equal to "
            "the Version 1.0 threshold of 50%."
        )


with col2:

    with st.container(
        border=True
    ):

        st.markdown(
            "### Less Likely Arrest"
        )

        st.write(
            "Arrest probability is below the Version 1.0 "
            "threshold of 50%."
        )


st.warning(
    "A High or Critical incident can still receive a "
    "'Less Likely Arrest' ML result. Arrest likelihood and "
    "operational priority represent different concepts."
)


st.divider()


# ============================================================
# TECHNICAL LIMITATIONS
# ============================================================

st.subheader(
    "05 · Technical Limitations"
)

st.markdown(
    """
- The primary model was trained using public Chicago police data rather
  than Indian Army Provost operational data.
- Model development used a 20% stratified sample because of Colab
  CPU/RAM constraints.
- Historical police data may contain geographic, reporting, institutional,
  and enforcement biases.
- The classification threshold remains fixed at 0.50.
- The current model output should not be interpreted as an autonomous
  operational recommendation.
"""
)


st.caption(
    "Version 1.1 Analytics is intended for supervisors, developers, "
    "and technical reviewers rather than routine operator decision-making."
)
