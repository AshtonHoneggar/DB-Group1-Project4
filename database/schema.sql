-- ----------------------------------------------------------------
-- Users
-- ----------------------------------------------------------------
CREATE TYPE USER_ROLE AS ENUM (
    'user',
    'it'
);

CREATE TABLE IF NOT EXISTS users (
    id              SERIAL PRIMARY KEY                       UNIQUE,
    firstname       VARCHAR(64)                              NOT NULL,
    lastname        VARCHAR(64)                              NOT NULL,
    email           VARCHAR(64)                              NOT NULL,
    managerID       REFERENCES users (id) ON DELETE CASCADE,
    role            USER_ROLE                                NOT NULL DEFAULT 'user',
    username        VARCHAR(64)                              UNIQUE NOT NULL,
    password        VARCHAR(64)                              NOT NULL
);

-- ----------------------------------------------------------------
-- Tickets
-- from professor feedback, no archive table. simply have query
-- to return closed tickets
-- ----------------------------------------------------------------
CREATE TYPE TICKET_STATUS AS ENUM (
    'open',
    'in_progress',
    'closed'
);

CREATE TYPE ISSUE_TYPE AS ENUM (
    'other',
    'another issue type',
    'another issue type'
);

CREATE TABLE IF NOT EXISTS tickets (
    id              SERIAL PRIMARY KEY UNIQUE,
    issue           ISSUE_TYPE         NOT NULL DEFAULT 'other',
    approved        BOOLEAN            NOT NULL DEFAULT FALSE,
    status          TICKET_STATUS      NOT NULL DEFAULT 'open',
    user_comment    VARCHAR(64)        NOT NULL,
    IT_comment      VARCHAR(64)        NOT NULL,
    date_opened     BIGINT             NOT NULL,
    date_closed     BIGINT
);

-- ----------------------------------------------------------------
-- Assigned
-- ----------------------------------------------------------------
CREATE TABLE IF NOT EXISTS assigned (
    reported_by     USER REFERENCES users (id) ON DELETE CASCADE     NOT NULL,
    assigned_to     IT REFERENCES users (id) ON DELETE CASCADE,
    ticket_id       TICKET REFERENCES tickets (id) ON DELETE CASCADE NOT NULL
)