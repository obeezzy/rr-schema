--- Create enums
CREATE TYPE PAYMENT_METHOD AS ENUM('cash', 'credit_card', 'debit_card');

-- Create business details table
CREATE TABLE business_details (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    business_family TEXT NOT NULL,
    establishment_year INTEGER NOT NULL,
    phone_number TEXT DEFAULT NULL,
    logo BYTEA,
    extra_details TEXT DEFAULT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create client table
CREATE TABLE client (
    id BIGSERIAL PRIMARY KEY,
    first_name TEXT DEFAULT NULL,
    last_name TEXT DEFAULT NULL,
    preferred_name TEXT NOT NULL,
    phone_number TEXT NOT NULL UNIQUE,
    alternate_phone_number TEXT DEFAULT NULL,
    address TEXT DEFAULT NULL,
    note_id BIGINT DEFAULT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL
);

-- Create credit payment table
CREATE TABLE credit_payment (
    id BIGSERIAL PRIMARY KEY,
    credit_transaction_id BIGINT NOT NULL,
    total_credit NUMERIC(19,2) NOT NULL,
    amount_paid NUMERIC(19,2) NOT NULL,
    balance NUMERIC(19,2) NOT NULL,
    currency TEXT NOT NULL,
    due_date_time TIMESTAMP NOT NULL,
    note_id BIGINT DEFAULT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL
);

-- Create creditor table
CREATE TABLE creditor (
    id BIGSERIAL PRIMARY KEY,
    client_id BIGINT NOT NULL,
    note_id BIGINT DEFAULT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL
);

-- Create credit transaction table
CREATE TABLE credit_transaction (
    id BIGSERIAL PRIMARY KEY,
    creditor_id BIGINT NOT NULL,
    transaction_table TEXT NOT NULL,
    transaction_id BIGINT DEFAULT NULL,
    note_id BIGINT DEFAULT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL
);

-- Create product quantity table
CREATE TABLE product_quantity (
    id BIGSERIAL PRIMARY KEY,
    product_id BIGINT NOT NULL UNIQUE,
    quantity REAL NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL
);

-- Create customer table
CREATE TABLE customer (
    id BIGSERIAL PRIMARY KEY,
    client_id BIGINT NOT NULL UNIQUE,
    note_id BIGINT DEFAULT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL
);

-- Create damaged quantity table
CREATE TABLE damaged_quantity (
    id BIGSERIAL PRIMARY KEY,
    product_id BIGINT DEFAULT NULL UNIQUE,
    quantity REAL NOT NULL,
    product_unit_id BIGINT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL
);

-- Create DB info table
CREATE TABLE db_info (
    version TEXT PRIMARY KEY,
    rack_id TEXT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create debt payment table
CREATE TABLE debt_payment (
    id BIGSERIAL PRIMARY KEY,
    debt_transaction_id BIGINT NOT NULL,
    total_debt NUMERIC(19,2) NOT NULL,
    amount_paid NUMERIC(19,2) NOT NULL,
    balance NUMERIC(19,2) NOT NULL,
    currency TEXT NOT NULL,
    due_date_time TIMESTAMP NOT NULL,
    note_id BIGINT DEFAULT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL
);

-- Create debt transaction table
CREATE TABLE debt_transaction (
    id BIGSERIAL PRIMARY KEY,
    debtor_id BIGINT NOT NULL,
    transaction_table TEXT NOT NULL,
    transaction_id BIGINT DEFAULT NULL,
    note_id BIGINT DEFAULT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL
);

-- Create debtor table
CREATE TABLE debtor (
    id BIGSERIAL PRIMARY KEY,
    client_id BIGINT NOT NULL,
    note_id BIGINT DEFAULT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL
);

-- Create expense transaction table
CREATE TABLE expense_transaction (
    id BIGSERIAL PRIMARY KEY,
    client_name TEXT NOT NULL,
    client_id BIGINT DEFAULT NULL,
    purpose TEXT NOT NULL,
    amount NUMERIC(19,2) NOT NULL,
    payment_method PAYMENT_METHOD NOT NULL DEFAULT 'cash',
    currency TEXT NOT NULL,
    note_id BIGINT DEFAULT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL
);

-- Create income transaction table
CREATE TABLE income_transaction (
    id BIGSERIAL PRIMARY KEY,
    client_name TEXT NOT NULL,
    client_id BIGINT DEFAULT NULL,
    purpose TEXT NOT NULL,
    amount NUMERIC(19,2) NOT NULL,
    payment_method PAYMENT_METHOD NOT NULL DEFAULT 'cash',
    currency TEXT NOT NULL,
    note_id BIGINT DEFAULT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL
);

-- Create product quantity snapshot table
CREATE TABLE product_quantity_snapshot (
    id BIGSERIAL PRIMARY KEY,
    product_id BIGINT NOT NULL,
    quantity REAL NOT NULL,
    reason TEXT NOT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL
);

-- Create last used date/time table
CREATE TABLE last_used_date_time (
    last_date_time TIMESTAMP NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (last_date_time)
);

-- Create note table
CREATE TABLE note (
    id BIGSERIAL PRIMARY KEY,
    note TEXT NOT NULL,
    table_name TEXT DEFAULT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL
);

-- Create product table
CREATE TABLE product (
    id BIGSERIAL PRIMARY KEY,
    product_category_id BIGINT NOT NULL,
    product TEXT NOT NULL,
    short_form TEXT DEFAULT NULL,
    description TEXT DEFAULT NULL,
    barcode TEXT DEFAULT NULL,
    divisible BOOLEAN DEFAULT TRUE,
    image BYTEA DEFAULT NULL,
    note_id BIGINT DEFAULT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL
);

-- Create product category table
CREATE TABLE product_category (
    id BIGSERIAL PRIMARY KEY,
    category TEXT NOT NULL UNIQUE,
    short_form TEXT DEFAULT NULL,
    note_id BIGINT DEFAULT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL
);

-- Create product_unit table
CREATE TABLE product_unit (
    id BIGSERIAL PRIMARY KEY,
    product_id BIGINT NOT NULL,
    unit TEXT NOT NULL,
    short_form TEXT DEFAULT NULL,
    preferred BOOLEAN NOT NULL DEFAULT FALSE,
    base_unit_equivalent REAL NOT NULL,
    cost_price NUMERIC(19,2) NOT NULL,
    retail_price NUMERIC(19,2) NOT NULL,
    currency TEXT NOT NULL,
    note_id BIGINT DEFAULT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL
);

-- Create purchased product table
CREATE TABLE purchased_product (
    id BIGSERIAL PRIMARY KEY,
    purchase_transaction_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    unit_price NUMERIC(19,2) NOT NULL,
    quantity REAL NOT NULL,
    product_unit_id BIGINT NOT NULL,
    cost NUMERIC(19,2) NOT NULL,
    discount NUMERIC(19,2) DEFAULT '0.00',
    currency TEXT NOT NULL,
    note_id BIGINT DEFAULT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL
);

-- Create purchase payment table
CREATE TABLE purchase_payment (
    id BIGSERIAL PRIMARY KEY,
    purchase_transaction_id BIGINT NOT NULL,
    amount NUMERIC(19,2) NOT NULL,
    payment_method PAYMENT_METHOD NOT NULL DEFAULT 'cash',
    currency TEXT NOT NULL,
    note_id BIGINT DEFAULT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL
);

-- Create purchase transaction table
CREATE TABLE purchase_transaction (
    id BIGSERIAL PRIMARY KEY,
    vendor_name TEXT NOT NULL,
    vendor_id BIGINT DEFAULT NULL,
    discount NUMERIC(19,2) NOT NULL DEFAULT '0.00',
    suspended BOOLEAN NOT NULL DEFAULT FALSE,
    note_id BIGINT DEFAULT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL
);

-- Create sold product table
CREATE TABLE sold_product (
    id BIGSERIAL PRIMARY KEY,
    sale_transaction_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    unit_price NUMERIC(19,2) NOT NULL,
    quantity REAL NOT NULL,
    product_unit_id BIGINT NOT NULL,
    cost NUMERIC(19,2) NOT NULL,
    discount NUMERIC(19,2) DEFAULT '0.00',
    currency TEXT NOT NULL,
    note_id BIGINT DEFAULT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL
);

-- Create sale payment table
CREATE TABLE sale_payment (
    id BIGSERIAL PRIMARY KEY,
    sale_transaction_id BIGINT NOT NULL,
    amount NUMERIC(19,2) NOT NULL,
    payment_method PAYMENT_METHOD NOT NULL DEFAULT 'cash',
    currency TEXT NOT NULL,
    note_id BIGINT DEFAULT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL
);

-- Create sale transaction table
CREATE TABLE sale_transaction (
    id BIGSERIAL PRIMARY KEY,
    customer_name TEXT NOT NULL,
    customer_id BIGINT DEFAULT NULL,
    discount NUMERIC(19,2) NOT NULL DEFAULT '0.00',
    suspended BOOLEAN NOT NULL DEFAULT FALSE,
    note_id BIGINT DEFAULT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL
);

-- Create unit relation table
CREATE TABLE unit_relation (
    id BIGSERIAL PRIMARY KEY,
    product_id BIGINT NOT NULL,
    old_unit_quantity REAL NOT NULL,
    old_unit_id BIGINT NOT NULL,
    new_unit_quantity REAL NOT NULL,
    new_unit_id BIGINT NOT NULL,
    note_id BIGINT NOT NULL DEFAULT 0,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL
);

-- Create user table
CREATE TABLE rr_user (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    photo BYTEA DEFAULT NULL,
    phone_number TEXT DEFAULT NULL,
    email_address TEXT DEFAULT NULL, active BOOLEAN DEFAULT FALSE, note_id BIGINT DEFAULT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL DEFAULT 0
);

-- Create user privilege table
CREATE TABLE user_privilege (
    user_id BIGINT PRIMARY KEY,
    privileges JSON NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create user privilege preset table
CREATE TABLE user_privilege_preset (
    id BIGSERIAL PRIMARY KEY,
    preset JSON NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL
);

-- Create vendor table
CREATE TABLE vendor (
    id BIGSERIAL PRIMARY KEY,
    client_id BIGINT NOT NULL UNIQUE,
    note_id BIGINT DEFAULT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL
);

-- Add admin user
INSERT INTO rr_user (username,
                    first_name,
                    last_name,
                    active,
                    user_id)
    VALUES ('admin',
            'admin',
            'admin',
            TRUE,
            1) 
