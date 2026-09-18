CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

CREATE TABLE IF NOT EXISTS hardware_events (
    time TIMESTAMPTZ NOT NULL,
    device_id UUID NOT NULL,
    hardware_type VARCHAR(32) NOT NULL,
    event_status VARCHAR(16) NOT NULL,
    duration_ms INT DEFAULT 0,
    encrypted_payload TEXT NOT NULL
);

-- Converts standard SQL table into a high-speed time-series hypertable
SELECT create_hypertable('hardware_events', 'time', if_not_exists => TRUE);