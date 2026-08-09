# 🛡️ Army Provost ML Project

## Control Room — Machine Learning Decision Support for Army Provost Functioning

**Author:** Arnav Sharma  
**Version:** 1.0  
**Status:** Functional Engineering Prototype  
**Development Environment:** Google Colab  
**Dashboard:** Streamlit  
**Prototype Deployment:** Cloudflare Quick Tunnel  

---

## 📌 Project Overview

The **Army Provost ML Project** is an engineering decision-support prototype that explores how **Machine Learning, structured incident classification, operational response mapping, and an interactive control-room dashboard** can support incident assessment in an Army Provost-oriented environment.

The system combines large-scale public crime-data analysis with a structured Decision Support System (DSS).

The completed Version 1.0 integrates:

- Large-scale crime-data preprocessing
- Exploratory Data Analysis (EDA)
- Machine Learning-based arrest-likelihood prediction
- Army Provost-oriented incident taxonomy
- Operational priority classification
- Recommended response mapping
- Structured response guidance
- Human-in-the-loop decision support
- Session-level recent decision history
- Persistent DSS audit logging
- Streamlit control-room dashboard
- Cloudflare Quick Tunnel deployment

> **Important:** This project is an academic and engineering prototype. It is **not an official Indian Army system**, does not implement classified or official operational SOPs, and is not intended to autonomously make command, legal, disciplinary, or operational decisions.

---

## 🎯 Problem Statement

Control-room environments may receive incidents that vary significantly in **type, urgency, location, context, and operational implications**.

A Decision Support System can help organize these inputs into a consistent assessment by combining:

1. Historical data patterns
2. Machine Learning inference
3. Structured incident classification
4. Deterministic operational mapping
5. Human operator oversight

The project therefore investigates whether a Machine Learning model trained using a large public crime dataset can be integrated with an Army Provost-oriented decision-support layer to provide:

- Incident classification
- Priority assessment
- Arrest-likelihood estimation
- Recommended response categories
- Structured operator guidance
- Traceable decision records

The system is designed to **support a human operator — not replace one**.

---

## 🎯 Project Objectives

The primary objectives of Version 1.0 are:

- Process and analyze large public crime datasets
- Identify temporal, geographic, incident-type, and arrest-related patterns
- Develop and compare supervised Machine Learning models
- Predict arrest likelihood from incident characteristics
- Translate public crime categories into an Army Provost-oriented taxonomy
- Assign operational priority levels
- Map incidents to recommended response categories
- Integrate ML inference with deterministic DSS logic
- Present results through an interactive Streamlit dashboard
- Provide structured prototype response guidance
- Maintain session-level recent decision history
- Persist DSS audit records across sessions
- Validate the complete system through functional, boundary, regression, and fresh-runtime testing

---

# 🏗️ System Architecture

## High-Level Workflow

```text
Public Police Datasets
        │
        ▼
Data Cleaning & Preprocessing
        │
        ▼
Exploratory Data Analysis
        │
        ▼
Feature Engineering
        │
        ▼
Machine Learning Model Development
        │
        ▼
Saved Random Forest + Preprocessing Pipeline
        │
        ├──────────────────────────────┐
        │                              │
        ▼                              ▼
Army Provost Taxonomy          Arrest-Likelihood Inference
        │                              │
        ▼                              │
Priority Mapping                       │
        │                              │
        └──────────────┬───────────────┘
                       │
                       ▼
              DSS Decision Layer
                       │
          ┌────────────┴─────────────┐
          │                          │
          ▼                          ▼
Operational Response         Structured Guidance
          │                          │
          └────────────┬─────────────┘
                       │
                       ▼
              Streamlit Dashboard
                       │
          ┌────────────┴─────────────┐
          │                          │
          ▼                          ▼
Session Decision History      Persistent Audit Log
                       │
                       ▼
             Cloudflare Quick Tunnel
```

---

# 📊 Dataset Overview

Two public police datasets were incorporated into the project.

## 1. Chicago Crimes Dataset

The **Chicago Crimes dataset** is the primary dataset used for Machine Learning development.

| Attribute | Value |
|---|---|
| Raw Records | **8,602,734** |
| Raw Columns | **22** |
| Primary ML Dataset | Yes |
| Target Variable | `Arrest` |
| Raw File | `Crimes_-_2001_to_Present_20260729.csv` |
| Cleaned File | `chicago_crimes_cleaned.csv` |

### Target Distribution

| Arrest | Count | Percentage |
|---|---:|---:|
| False | 6,449,253 | 74.97% |
| True | 2,153,481 | 25.03% |

Because of the CPU and RAM constraints of the Google Colab environment, model development used a **20% stratified sample**.

This produced approximately:

- **1,720,546 modeling records**
- **1,376,436 training records**
- **344,110 testing records**

The target distribution was preserved during sampling.

---

## 2. Montgomery County Dispatch Dataset

A Montgomery County police dispatch dataset was incorporated as a secondary dataset for exploratory analysis.

| Attribute | Value |
|---|---|
| Records | **1,886,836** |
| Columns | **26** |
| Role | Secondary EDA dataset |
| Cleaned File | `montgomery_dispatch_cleaned.csv` |

The deployed Version 1.0 arrest-likelihood model is based on the **Chicago Crimes dataset**.

---

# 📁 Project Directory Structure

The project uses a fixed Google Drive directory structure:

```text
/content/drive/MyDrive/Army_Provost_ML_Project/
│
├── Datasets/
│   ├── Raw/
│   └── Cleaned/
│
├── Notebooks/
│
├── Models/
│
├── Figures/
│
├── Reports/
│
├── Outputs/
│
└── Logs/
```

The directory structure and root path are intentionally kept constant throughout development to maintain reproducibility across Google Colab runtime resets.

---

# 🧹 Data Preprocessing

The Machine Learning pipeline uses both categorical and numerical incident features.

## Categorical Features

- `Primary Type`
- `Location Description`
- `Domestic`

## Numerical Features

- `Year`
- `Month`
- `Day`
- `Hour`
- `District`
- `Beat`
- `Ward`
- `Community Area`

The `Description` feature was excluded from the final model feature set because of its comparatively high cardinality.

After preprocessing and encoding, the final Machine Learning feature space contained:

**231 encoded features**

The fitted preprocessing pipeline was saved so dashboard inference uses the **same transformations used during model development**.

---

# 📈 Exploratory Data Analysis

EDA was performed to identify important patterns within the datasets.

Major analyses included:

- Most frequent crime categories
- Year-wise crime trends
- Monthly crime distribution
- Day-of-week patterns
- Hour-wise crime distribution
- District-wise distribution
- Common incident locations
- Domestic vs non-domestic incidents
- Arrest-related patterns

## Major Chicago Incident Categories

| Incident Type | Number of Incidents |
|---|---:|
| THEFT | 1,827,377 |
| BATTERY | 1,567,212 |
| CRIMINAL DAMAGE | 977,357 |
| NARCOTICS | 768,704 |
| ASSAULT | 580,094 |
| OTHER OFFENSE | 537,540 |
| BURGLARY | 455,436 |
| MOTOR VEHICLE THEFT | 444,725 |
| DECEPTIVE PRACTICE | 400,071 |
| ROBBERY | 318,103 |

Major incident locations included:

- STREET
- RESIDENCE
- APARTMENT
- SIDEWALK

EDA figures generated during the project are stored in the `Figures/` directory.

---

# 🤖 Machine Learning Methodology

The Machine Learning problem is formulated as a **binary classification task**.

```text
Arrest = True  → Positive Class
Arrest = False → Negative Class
```

Three primary supervised Machine Learning algorithms were evaluated:

1. **Logistic Regression**
2. **Random Forest**
3. **CatBoost**

Because `Arrest = True` represents the positive class, model selection was **not based on accuracy alone**.

Recall, precision, F1 score, ROC-AUC, computational requirements, and integration stability were also considered.

---

# 📊 Model Performance Comparison

| Model | Accuracy | Precision | Recall | F1 Score | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.8301 | 0.6539 | **0.6824** | 0.6678 | 0.8748 |
| **Random Forest** | **0.8672** | **0.7733** | **0.6640** | **0.7145** | **0.8882** |
| CatBoost | 0.8838 | 0.8955 | 0.6065 | 0.7232 | 0.8981 |

---

## 🌲 Final Version 1.0 Model — Random Forest

CatBoost achieved the highest:

- Accuracy
- Precision
- F1 Score
- ROC-AUC

However, its positive-class recall was **0.6065**, compared with:

- Logistic Regression — **0.6824**
- Random Forest — **0.6640**

The baseline Random Forest was retained for Version 1.0 after considering:

- Positive-class performance
- Balanced overall metrics
- Operational emphasis of the project
- Validated preprocessing and inference pipeline
- CPU-only computational constraints
- Integration stability within the DSS

Therefore, Random Forest is **not presented as universally superior to every tested model**.

It represents the selected **Version 1.0 engineering trade-off**.

---

## Random Forest Confusion Matrix

```text
[[241206, 16765],
 [ 28942, 57197]]
```

---

## Saved ML Artifacts

```text
Models/final_random_forest.pkl
Models/preprocessing_pipeline.pkl
```

The operational classification threshold remains:

```text
0.50
```

No threshold optimization was applied in Version 1.0.

---

# 🔍 Random Forest Feature Importance

Aggregated Random Forest feature importance showed that incident type was the dominant predictive feature.

| Feature | Importance |
|---|---:|
| Primary Type | 0.690081 |
| Location Description | 0.146424 |
| Year | 0.040612 |
| Hour | 0.025643 |
| Domestic | 0.020923 |
| Beat | 0.017048 |
| Community Area | 0.013996 |
| Ward | 0.012781 |
| Day | 0.011749 |
| District | 0.011255 |
| Month | 0.009486 |

> Feature importance describes the behavior of the trained model. It should **not** be interpreted as evidence of causation.

---

# 🪖 Army Provost Operational Taxonomy

Public police incident categories are translated into a conceptual Army Provost-oriented taxonomy.

```text
Public Incident Type
        │
        ▼
Provost Incident Category
        │
        ▼
Incident Subcategory
        │
        ▼
Operational Priority
        │
        ▼
Recommended Response Type
```

This architecture deliberately separates:

**Machine Learning inference**

from

**Domain-oriented operational classification**

The ML model predicts arrest likelihood, while deterministic mappings determine how the incident is categorized and presented within the prototype DSS.

---

# 🧠 Decision Support System

The DSS combines **Machine Learning inference** with **deterministic operational logic**.

## Machine Learning Layer

The Random Forest estimates:

**Arrest Probability (%)**

Using the fixed Version 1.0 threshold of `0.50`, the probability is converted into:

```text
Likely Arrest
```

or

```text
Less Likely Arrest
```

---

## Operational Decision Layer

The deterministic DSS layer determines:

- Provost Incident Category
- Incident Subcategory
- Priority
- Recommended Response Type
- Structured Response Guidance

This separation prevents the ML probability from being treated as the sole basis for an operational recommendation.

---

# 📋 Structured Response Guidance

Version 1.0 provides structured prototype guidance under four categories:

### 1. Immediate Operator Guidance

Initial actions that may assist the operator in handling the reported incident.

### 2. Coordination / Notification

Relevant coordination and notification considerations.

### 3. Scene / Evidence Considerations

Guidance relating to information preservation, scene awareness, and evidence considerations.

### 4. Escalation / Follow-up

Considerations for supervisory escalation and subsequent follow-up.

All guidance is explicitly identified as:

> **Prototype Decision-Support Guidance**

It does not represent official operational SOP.

---

# 🖥️ Streamlit Control-Room Dashboard

The final system provides an interactive Streamlit interface for entering incident information and reviewing the DSS assessment.

## Operator Inputs

The dashboard accepts:

- Incident Type
- Location Description
- Domestic Incident
- Year
- Month
- Day
- Hour
- District
- Beat
- Ward
- Community Area

## DSS Outputs

Following successful analysis, the dashboard displays:

- Provost Incident Category
- Incident Subcategory
- Priority
- Arrest Probability
- ML Assessment
- Recommended Response Type
- Structured Response Guidance
- Decision ID
- Decision Timestamp
- Recent Decision History
- Persistent Audit Status

---

## 📷 Dashboard Screenshot

**Final Version 1.0 dashboard screenshot will be added here.**

After adding the image to the repository, this section can use:

```markdown
![Army Provost DSS Dashboard](Figures/Army_Provost_Dashboard_V1.png)
```

---

# 🕘 Session-Level Recent Decision History

The dashboard maintains a lightweight recent-decision history using:

```python
st.session_state
```

Version 1.0 stores the **20 most recent decisions** from the active Streamlit session.

Each history record contains:

- Decision ID
- Timestamp
- Incident Type
- Priority
- Arrest Probability
- ML Assessment
- Recommended Response Type

The newest decision appears first.

> Session history is intentionally cleared when the Streamlit session ends.

---

# 🗃️ Persistent DSS Audit Logging

Successful analyses are also appended to a persistent CSV audit trail:

```text
Logs/Army_Provost_DSS_Audit_Log.csv
```

The audit record contains:

- Decision ID
- Decision Timestamp
- Incident inputs
- Provost classification
- Priority
- Arrest Probability
- ML Assessment
- Recommended Response
- Structured Response Guidance

Persistent logging was verified across a **fresh Google Colab runtime restart**.

> The audit trail records system-generated DSS outputs. It should not be interpreted as an authoritative record of a human operator's final operational decision.

---

# 🌐 Deployment Architecture

Version 1.0 is developed and executed using Google Colab.

```text
Google Drive
     │
     ▼
Persistent Project Files
     │
     ▼
Google Colab Runtime
     │
     ▼
Streamlit Server
     │
     ▼
localhost:8501
     │
     ▼
Cloudflare Quick Tunnel
     │
     ▼
Temporary Public HTTPS URL
```

Cloudflare Quick Tunnel provides temporary external access to the Streamlit application.

> A new tunnel may generate a new URL after a Colab runtime restart.

---

# ✅ Version 1.0 Validation

The completed system underwent four final validation phases.

---

## Phase A — Functional Validation

Six representative incident scenarios were evaluated:

- BATTERY
- ARSON
- THEFT
- NARCOTICS
- WEAPONS VIOLATION
- HOMICIDE

### Result

```text
Scenario Execution        : 6/6 PASS
Structured Guidance       : 6/6 PASS
Decision Record           : 6/6 PASS
BATTERY Golden Regression : PASS
```

### Representative Outputs

| Incident | Priority | Arrest Probability | ML Assessment |
|---|---|---:|---|
| BATTERY | High | 39.57% | Less Likely Arrest |
| ARSON | High | 40.57% | Less Likely Arrest |
| THEFT | Moderate | 19.97% | Less Likely Arrest |
| NARCOTICS | High | 91.13% | Likely Arrest |
| WEAPONS VIOLATION | High | 79.82% | Likely Arrest |
| HOMICIDE | Critical | 51.77% | Likely Arrest |

**Phase A Result: PASS ✅**

---

## Phase B — Boundary & Error Validation

Boundary conditions tested included:

- Month lower boundary
- Month upper boundary
- Hour lower boundary
- Hour upper boundary
- Administrative zero boundary
- `Domestic = True`

Invalid inputs tested included:

- Month = 13
- Month = 0
- Hour = 24
- Unknown incident type

All tested boundary conditions and invalid inputs behaved as expected.

**Phase B Result: PASS ✅**

---

## Phase C — Regression Validation

The established BATTERY golden regression case remained:

```text
Incident Type        : BATTERY
Arrest Probability   : 39.57%
ML Assessment        : Less Likely Arrest
Priority             : High
Recommended Response : Personnel Safety / Provost Response
```

**Phase C Result: PASS ✅**

---

## Phase D — Fresh Runtime & Deployment Validation

The complete project was restarted from a fresh Google Colab runtime.

The system successfully restored:

- Google Drive project paths
- Persistent DSS backend
- Runtime dependencies
- Saved ML model
- Preprocessing pipeline
- Streamlit dashboard
- Cloudflare tunnel deployment
- DSS inference
- Session decision history
- Persistent audit logging

A new incident was successfully analyzed after restart and appended to the existing persistent audit log.

**Phase D Result: PASS ✅**

---

# 📦 Key Project Artifacts

## Machine Learning Models

```text
Models/final_random_forest.pkl
Models/preprocessing_pipeline.pkl
```

## Important Outputs

```text
Outputs/Final_Model_Performance_Comparison.csv
Outputs/Random_Forest_Top20_Feature_Importance.csv
Outputs/Random_Forest_Aggregated_Feature_Importance.csv
Outputs/army_provost_dss_backend.py
Outputs/army_provost_dashboard.py
```

## Audit Log

```text
Logs/Army_Provost_DSS_Audit_Log.csv
```

## Important Figures

```text
Figures/Top15_Chicago_Crime_Categories.png
Figures/Yearwise_Crime_Trend.png
Figures/Monthly_Crime_Distribution.png
Figures/DayOfWeek_Crime_Distribution.png
Figures/Hourwise_Crime_Distribution.png
Figures/Districtwise_Crime_Distribution.png
Figures/Top15_Crime_Locations.png
Figures/Random_Forest_Top20_Feature_Importance.png
Figures/Random_Forest_Aggregated_Feature_Importance.png
Figures/Model_Performance_Comparison.png
```

---

# 🚀 Running Version 1.0

The project is designed to run in **Google Colab**.

## Startup Sequence

1. Open the final dashboard notebook from the `Notebooks/` directory.
2. Mount Google Drive.
3. Verify the fixed project paths.
4. Import the persistent DSS backend.
5. Restore Streamlit dependencies.
6. Generate and validate the Streamlit application.
7. Restore `cloudflared` if required.
8. Start or reuse Streamlit on port `8501`.
9. Create the Cloudflare Quick Tunnel.
10. Open the newly generated HTTPS URL.
11. Enter incident details.
12. Select **ANALYZE INCIDENT**.

Because the trained model and preprocessing pipeline are stored persistently in Google Drive:

> **Model retraining is not required to launch Version 1.0.**

---

# 🛠️ Technology Stack

## Data Science & Machine Learning

- Python
- Pandas
- NumPy
- Scikit-learn
- CatBoost
- Joblib

## Data Visualization

- Matplotlib
- Plotly

## Dashboard

- Streamlit
- HTML/CSS

## Development & Storage

- Google Colab
- Google Drive

## Version Control

- Git
- GitHub

## Prototype Deployment

- Cloudflare Quick Tunnel

---

# ⚠️ Current Limitations

Version 1.0 has several important limitations:

1. The primary ML model is trained on **Chicago public police data**, not Indian Army Provost operational data.
2. The Army Provost taxonomy and response guidance are conceptual prototype mappings rather than official SOP.
3. Model development used a **20% stratified sample** because of CPU and RAM constraints.
4. The deployed classification threshold remains fixed at **0.50**.
5. Arrest likelihood must not be interpreted as guilt, threat level, legal outcome, or required operational action.
6. Historical public-police data may contain geographic, institutional, reporting, and enforcement biases.
7. Cloudflare Quick Tunnel URLs are temporary.
8. CSV audit logging is suitable for a prototype but is not a production-grade secure audit database.
9. Version 1.0 does not implement production authentication, role-based access control, or enterprise security controls.
10. The system depends on compatibility between its saved preprocessing pipeline and trained model.

---

# 🔮 Future Scope

Potential future improvements include:

- Validation using more operationally representative and appropriately authorized datasets
- Full-dataset model development using higher-compute infrastructure
- Probability calibration
- Decision-threshold analysis
- Cost-sensitive learning
- Additional class-imbalance strategies
- Temporal validation
- Geographic validation
- Systematic fairness and bias assessment
- Individual-prediction explainability
- Role-based authentication
- Secure database-backed audit logging
- Persistent production deployment
- Operator feedback mechanisms
- Human-factors and usability evaluation
- Formal domain-expert validation of taxonomy and response guidance

---

# ⚖️ Responsible Use

This repository demonstrates an **academic Machine Learning and Decision Support System architecture**.

Model output must **not** be used as an autonomous basis for:

- Arrest or detention
- Disciplinary action
- Legal judgment
- Personnel evaluation
- Threat designation
- Operational command decisions

Any real-world implementation would require:

- Authorized and representative data
- Appropriate legal and policy review
- Domain-expert validation
- Security controls
- Human oversight
- Formal operational testing

Human judgment and authorized procedures must remain the controlling factors.

---

# 🏁 Version 1.0 Status

## ✅ Functional Engineering Prototype

Version 1.0 includes:

- ✅ Large-scale crime-data preprocessing
- ✅ Exploratory Data Analysis
- ✅ Machine Learning model comparison
- ✅ Saved Random Forest inference pipeline
- ✅ Army Provost-oriented incident taxonomy
- ✅ Operational priority mapping
- ✅ Recommended response mapping
- ✅ Structured response guidance
- ✅ Persistent DSS backend
- ✅ Streamlit control-room dashboard
- ✅ Session-level recent decision history
- ✅ Persistent DSS audit logging
- ✅ Cloudflare prototype deployment
- ✅ Functional validation
- ✅ Boundary and error validation
- ✅ Golden regression validation
- ✅ Fresh-runtime reproducibility validation

---

# 👤 Author

**Arnav Sharma**

---

### Army Provost ML Project — Version 1.0
