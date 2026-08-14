-- Army Provost DSS — Synthetic Response Team Seed
-- Academic Prototype — No Real Operational Resources

INSERT INTO response_teams (
    team_id,
    team_name,
    status,
    current_zone,
    primary_capability,
    secondary_capabilities,
    readiness_level,
    personnel_strength,
    vehicle_available,
    capability_tags,
    current_assignment,
    last_updated
)
VALUES (
    'RT-01',
    'Response Team 01',
    'AVAILABLE',
    'Zone A',
    'Access and Perimeter Security',
    'Incident Control; Personnel Safety',
    'READY',
    6,
    TRUE,
    'Entry Control; Restricted Area Support',
    NULL,
    CURRENT_TIMESTAMP
)
ON CONFLICT (team_id)
DO UPDATE SET

    team_name = EXCLUDED.team_name,

    status = EXCLUDED.status,

    current_zone = EXCLUDED.current_zone,

    primary_capability =
        EXCLUDED.primary_capability,

    secondary_capabilities =
        EXCLUDED.secondary_capabilities,

    readiness_level =
        EXCLUDED.readiness_level,

    personnel_strength =
        EXCLUDED.personnel_strength,

    vehicle_available =
        EXCLUDED.vehicle_available,

    capability_tags =
        EXCLUDED.capability_tags,

    current_assignment =
        EXCLUDED.current_assignment,

    last_updated =
        CURRENT_TIMESTAMP;

INSERT INTO response_teams (
    team_id,
    team_name,
    status,
    current_zone,
    primary_capability,
    secondary_capabilities,
    readiness_level,
    personnel_strength,
    vehicle_available,
    capability_tags,
    current_assignment,
    last_updated
)
VALUES (
    'RT-02',
    'Response Team 02',
    'AVAILABLE',
    'Zone B',
    'Personnel Safety',
    'Incident Control; Medical Coordination',
    'READY',
    7,
    TRUE,
    'Personnel Protection; Immediate Response',
    NULL,
    CURRENT_TIMESTAMP
)
ON CONFLICT (team_id)
DO UPDATE SET

    team_name = EXCLUDED.team_name,

    status = EXCLUDED.status,

    current_zone = EXCLUDED.current_zone,

    primary_capability =
        EXCLUDED.primary_capability,

    secondary_capabilities =
        EXCLUDED.secondary_capabilities,

    readiness_level =
        EXCLUDED.readiness_level,

    personnel_strength =
        EXCLUDED.personnel_strength,

    vehicle_available =
        EXCLUDED.vehicle_available,

    capability_tags =
        EXCLUDED.capability_tags,

    current_assignment =
        EXCLUDED.current_assignment,

    last_updated =
        CURRENT_TIMESTAMP;

INSERT INTO response_teams (
    team_id,
    team_name,
    status,
    current_zone,
    primary_capability,
    secondary_capabilities,
    readiness_level,
    personnel_strength,
    vehicle_available,
    capability_tags,
    current_assignment,
    last_updated
)
VALUES (
    'RT-03',
    'Response Team 03',
    'OFFLINE',
    'Zone C',
    'Vehicle and Mobility Security',
    'Traffic and Movement Control; Incident Control',
    'UNAVAILABLE',
    5,
    FALSE,
    'Vehicle Security; Route Control',
    NULL,
    CURRENT_TIMESTAMP
)
ON CONFLICT (team_id)
DO UPDATE SET

    team_name = EXCLUDED.team_name,

    status = EXCLUDED.status,

    current_zone = EXCLUDED.current_zone,

    primary_capability =
        EXCLUDED.primary_capability,

    secondary_capabilities =
        EXCLUDED.secondary_capabilities,

    readiness_level =
        EXCLUDED.readiness_level,

    personnel_strength =
        EXCLUDED.personnel_strength,

    vehicle_available =
        EXCLUDED.vehicle_available,

    capability_tags =
        EXCLUDED.capability_tags,

    current_assignment =
        EXCLUDED.current_assignment,

    last_updated =
        CURRENT_TIMESTAMP;

INSERT INTO response_teams (
    team_id,
    team_name,
    status,
    current_zone,
    primary_capability,
    secondary_capabilities,
    readiness_level,
    personnel_strength,
    vehicle_available,
    capability_tags,
    current_assignment,
    last_updated
)
VALUES (
    'RT-04',
    'Response Team 04',
    'AVAILABLE',
    'Zone D',
    'Property and Asset Security',
    'Incident Control; Access and Perimeter Security',
    'READY',
    6,
    TRUE,
    'Stores Security; Asset Protection',
    NULL,
    CURRENT_TIMESTAMP
)
ON CONFLICT (team_id)
DO UPDATE SET

    team_name = EXCLUDED.team_name,

    status = EXCLUDED.status,

    current_zone = EXCLUDED.current_zone,

    primary_capability =
        EXCLUDED.primary_capability,

    secondary_capabilities =
        EXCLUDED.secondary_capabilities,

    readiness_level =
        EXCLUDED.readiness_level,

    personnel_strength =
        EXCLUDED.personnel_strength,

    vehicle_available =
        EXCLUDED.vehicle_available,

    capability_tags =
        EXCLUDED.capability_tags,

    current_assignment =
        EXCLUDED.current_assignment,

    last_updated =
        CURRENT_TIMESTAMP;

INSERT INTO response_teams (
    team_id,
    team_name,
    status,
    current_zone,
    primary_capability,
    secondary_capabilities,
    readiness_level,
    personnel_strength,
    vehicle_available,
    capability_tags,
    current_assignment,
    last_updated
)
VALUES (
    'RT-05',
    'Response Team 05',
    'AVAILABLE',
    'Zone E',
    'Personnel Safety',
    'Incident Control; Investigation Support',
    'LIMITED',
    5,
    TRUE,
    'Personnel Protection; Investigation Support',
    NULL,
    CURRENT_TIMESTAMP
)
ON CONFLICT (team_id)
DO UPDATE SET

    team_name = EXCLUDED.team_name,

    status = EXCLUDED.status,

    current_zone = EXCLUDED.current_zone,

    primary_capability =
        EXCLUDED.primary_capability,

    secondary_capabilities =
        EXCLUDED.secondary_capabilities,

    readiness_level =
        EXCLUDED.readiness_level,

    personnel_strength =
        EXCLUDED.personnel_strength,

    vehicle_available =
        EXCLUDED.vehicle_available,

    capability_tags =
        EXCLUDED.capability_tags,

    current_assignment =
        EXCLUDED.current_assignment,

    last_updated =
        CURRENT_TIMESTAMP;

INSERT INTO response_teams (
    team_id,
    team_name,
    status,
    current_zone,
    primary_capability,
    secondary_capabilities,
    readiness_level,
    personnel_strength,
    vehicle_available,
    capability_tags,
    current_assignment,
    last_updated
)
VALUES (
    'RT-06',
    'Response Team 06',
    'ASSIGNED',
    'Zone F',
    'Controlled Substances Response',
    'Incident Control; Investigation Support',
    'READY',
    6,
    TRUE,
    'Controlled Substance Handling; Evidence Support',
    'SIM-INC-0042',
    CURRENT_TIMESTAMP
)
ON CONFLICT (team_id)
DO UPDATE SET

    team_name = EXCLUDED.team_name,

    status = EXCLUDED.status,

    current_zone = EXCLUDED.current_zone,

    primary_capability =
        EXCLUDED.primary_capability,

    secondary_capabilities =
        EXCLUDED.secondary_capabilities,

    readiness_level =
        EXCLUDED.readiness_level,

    personnel_strength =
        EXCLUDED.personnel_strength,

    vehicle_available =
        EXCLUDED.vehicle_available,

    capability_tags =
        EXCLUDED.capability_tags,

    current_assignment =
        EXCLUDED.current_assignment,

    last_updated =
        CURRENT_TIMESTAMP;

INSERT INTO response_teams (
    team_id,
    team_name,
    status,
    current_zone,
    primary_capability,
    secondary_capabilities,
    readiness_level,
    personnel_strength,
    vehicle_available,
    capability_tags,
    current_assignment,
    last_updated
)
VALUES (
    'RT-07',
    'Response Team 07',
    'AVAILABLE',
    'Zone G',
    'Investigation Support',
    'Incident Control; Property and Asset Security',
    'READY',
    4,
    TRUE,
    'Evidence Preservation; Documentation',
    NULL,
    CURRENT_TIMESTAMP
)
ON CONFLICT (team_id)
DO UPDATE SET

    team_name = EXCLUDED.team_name,

    status = EXCLUDED.status,

    current_zone = EXCLUDED.current_zone,

    primary_capability =
        EXCLUDED.primary_capability,

    secondary_capabilities =
        EXCLUDED.secondary_capabilities,

    readiness_level =
        EXCLUDED.readiness_level,

    personnel_strength =
        EXCLUDED.personnel_strength,

    vehicle_available =
        EXCLUDED.vehicle_available,

    capability_tags =
        EXCLUDED.capability_tags,

    current_assignment =
        EXCLUDED.current_assignment,

    last_updated =
        CURRENT_TIMESTAMP;

INSERT INTO response_teams (
    team_id,
    team_name,
    status,
    current_zone,
    primary_capability,
    secondary_capabilities,
    readiness_level,
    personnel_strength,
    vehicle_available,
    capability_tags,
    current_assignment,
    last_updated
)
VALUES (
    'RT-08',
    'Response Team 08',
    'AVAILABLE',
    'Zone H',
    'Sensitive Incident Response',
    'Access and Perimeter Security; Incident Control',
    'READY',
    6,
    TRUE,
    'Restricted Area Support; Sensitive Incident Handling',
    NULL,
    CURRENT_TIMESTAMP
)
ON CONFLICT (team_id)
DO UPDATE SET

    team_name = EXCLUDED.team_name,

    status = EXCLUDED.status,

    current_zone = EXCLUDED.current_zone,

    primary_capability =
        EXCLUDED.primary_capability,

    secondary_capabilities =
        EXCLUDED.secondary_capabilities,

    readiness_level =
        EXCLUDED.readiness_level,

    personnel_strength =
        EXCLUDED.personnel_strength,

    vehicle_available =
        EXCLUDED.vehicle_available,

    capability_tags =
        EXCLUDED.capability_tags,

    current_assignment =
        EXCLUDED.current_assignment,

    last_updated =
        CURRENT_TIMESTAMP;

INSERT INTO response_teams (
    team_id,
    team_name,
    status,
    current_zone,
    primary_capability,
    secondary_capabilities,
    readiness_level,
    personnel_strength,
    vehicle_available,
    capability_tags,
    current_assignment,
    last_updated
)
VALUES (
    'RT-09',
    'Response Team 09',
    'AVAILABLE',
    'Zone C',
    'Vehicle and Mobility Security',
    'Traffic and Movement Control; Incident Control',
    'READY',
    6,
    TRUE,
    'Vehicle Security; Traffic Control',
    NULL,
    CURRENT_TIMESTAMP
)
ON CONFLICT (team_id)
DO UPDATE SET

    team_name = EXCLUDED.team_name,

    status = EXCLUDED.status,

    current_zone = EXCLUDED.current_zone,

    primary_capability =
        EXCLUDED.primary_capability,

    secondary_capabilities =
        EXCLUDED.secondary_capabilities,

    readiness_level =
        EXCLUDED.readiness_level,

    personnel_strength =
        EXCLUDED.personnel_strength,

    vehicle_available =
        EXCLUDED.vehicle_available,

    capability_tags =
        EXCLUDED.capability_tags,

    current_assignment =
        EXCLUDED.current_assignment,

    last_updated =
        CURRENT_TIMESTAMP;

INSERT INTO response_teams (
    team_id,
    team_name,
    status,
    current_zone,
    primary_capability,
    secondary_capabilities,
    readiness_level,
    personnel_strength,
    vehicle_available,
    capability_tags,
    current_assignment,
    last_updated
)
VALUES (
    'RT-10',
    'Response Team 10',
    'AVAILABLE',
    'Zone A',
    'Controlled Substances Response',
    'Investigation Support; Incident Control',
    'LIMITED',
    5,
    FALSE,
    'Evidence Support; Controlled Substance Response',
    NULL,
    CURRENT_TIMESTAMP
)
ON CONFLICT (team_id)
DO UPDATE SET

    team_name = EXCLUDED.team_name,

    status = EXCLUDED.status,

    current_zone = EXCLUDED.current_zone,

    primary_capability =
        EXCLUDED.primary_capability,

    secondary_capabilities =
        EXCLUDED.secondary_capabilities,

    readiness_level =
        EXCLUDED.readiness_level,

    personnel_strength =
        EXCLUDED.personnel_strength,

    vehicle_available =
        EXCLUDED.vehicle_available,

    capability_tags =
        EXCLUDED.capability_tags,

    current_assignment =
        EXCLUDED.current_assignment,

    last_updated =
        CURRENT_TIMESTAMP;