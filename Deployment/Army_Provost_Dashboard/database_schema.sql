
-- =====================================================================
-- ARMY PROVOST DSS — DEPLOYMENT DATABASE SCHEMA
-- Academic Prototype
-- =====================================================================


-- =====================================================================
-- 1. OPERATORS
-- =====================================================================

CREATE TABLE IF NOT EXISTS operators (

    operator_uid TEXT PRIMARY KEY,

    password_hash TEXT NOT NULL,

    display_name TEXT,

    created_at TIMESTAMPTZ
        DEFAULT CURRENT_TIMESTAMP,

    is_active BOOLEAN
        DEFAULT TRUE
);


-- =====================================================================
-- 2. RESPONSE TEAM REGISTRY
-- =====================================================================

CREATE TABLE IF NOT EXISTS response_teams (

    team_id TEXT PRIMARY KEY,

    team_name TEXT NOT NULL,

    status TEXT NOT NULL,

    current_zone TEXT NOT NULL,

    primary_capability TEXT NOT NULL,

    secondary_capabilities TEXT,

    readiness_level TEXT NOT NULL,

    personnel_strength INTEGER NOT NULL,

    vehicle_available BOOLEAN NOT NULL,

    capability_tags TEXT,

    current_assignment TEXT,

    last_updated TIMESTAMPTZ
        DEFAULT CURRENT_TIMESTAMP
);


-- =====================================================================
-- 3. DSS INCIDENT AUDIT
-- =====================================================================

CREATE TABLE IF NOT EXISTS dss_incident_audit (

    id BIGSERIAL PRIMARY KEY,

    decision_id TEXT UNIQUE NOT NULL,

    decision_timestamp TIMESTAMPTZ,

    primary_type TEXT,

    location_description TEXT,

    domestic BOOLEAN,

    provost_incident_category TEXT,

    incident_subcategory TEXT,

    priority TEXT,

    arrest_probability DOUBLE PRECISION,

    arrest_probability_percent DOUBLE PRECISION,

    arrest_prediction TEXT,

    recommended_response_type TEXT,

    year INTEGER,

    month INTEGER,

    day INTEGER,

    hour INTEGER,

    district INTEGER,

    beat INTEGER,

    ward INTEGER,

    community_area INTEGER,

    operator_uid TEXT
);


-- =====================================================================
-- 4. RESOURCE ALLOCATION AUDIT
-- =====================================================================

CREATE TABLE IF NOT EXISTS resource_allocation_audit (

    id BIGSERIAL PRIMARY KEY,

    decision_id TEXT UNIQUE NOT NULL,

    incident_id TEXT,

    decision_timestamp TIMESTAMPTZ,

    operator_uid TEXT,

    operational_response TEXT,

    incident_zone TEXT,

    required_capability TEXT,

    recommended_team_id TEXT,

    recommended_team_score DOUBLE PRECISION,

    operator_action TEXT,

    selected_team_id TEXT,

    selected_team_score DOUBLE PRECISION,

    override_reason TEXT
);


-- =====================================================================
-- INDEXES
-- =====================================================================

CREATE INDEX IF NOT EXISTS idx_dss_audit_timestamp
ON dss_incident_audit(decision_timestamp);


CREATE INDEX IF NOT EXISTS idx_resource_audit_timestamp
ON resource_allocation_audit(decision_timestamp);


CREATE INDEX IF NOT EXISTS idx_resource_operator
ON resource_allocation_audit(operator_uid);


CREATE INDEX IF NOT EXISTS idx_resource_selected_team
ON resource_allocation_audit(selected_team_id);
