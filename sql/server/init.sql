-- Create business admin table
CREATE TABLE IF NOT EXISTS business_admin (
    id BIGSERIAL PRIMARY KEY,
    email_address TEXT NOT NULL UNIQUE,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    phone_number TEXT,
    photo BYTEA,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    linked BOOLEAN NOT NULL DEFAULT FALSE,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created DATETIME NOT NULL,
    last_edited DATETIME NOT NULL
);

-- Create business store table
CREATE TABLE IF NOT EXISTS business_store (
    id BIGSERIAL PRIMARY KEY,
    business_admin_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    rack_id TEXT NOT NULL UNIQUE,
    address TEXT NOT NULL,
    location POINT, 
    business_family TEXT NOT NULL,
    establishment_year INTEGER DEFAULT NULL,
    phone_number TEXT DEFAULT NULL,
    logo BYTEA,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    linked BOOLEAN NOT NULL DEFAULT FALSE,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created DATETIME NOT NULL,
    last_edited DATETIME NOT NULL
);
