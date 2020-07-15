--- Create enums
CREATE TYPE PAYMENT_METHOD AS ENUM('cash', 'credit_card', 'debit_card');

-- Create business details table
CREATE TABLE business_details (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(200) NOT NULL,
    business_family VARCHAR(500) NOT NULL,
    establishment_year INTEGER NOT NULL,
    phone_number VARCHAR(20) DEFAULT NULL,
    logo BYTEA,
    extra_details VARCHAR(100) DEFAULT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create client table
CREATE TABLE client (
    id BIGSERIAL PRIMARY KEY,
    first_name VARCHAR(100) DEFAULT NULL,
    last_name VARCHAR(100) DEFAULT NULL,
    preferred_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) NOT NULL UNIQUE,
    alternate_phone_number VARCHAR(20) DEFAULT NULL,
    address VARCHAR(100) DEFAULT NULL,
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
    total_credit MONEY NOT NULL,
    amount_paid MONEY NOT NULL,
    balance MONEY NOT NULL,
    currency VARCHAR(4) NOT NULL,
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
    transaction_table VARCHAR(20) NOT NULL,
    transaction_id BIGINT DEFAULT NULL,
    note_id BIGINT DEFAULT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL
);

-- Create current product quantity table
CREATE TABLE current_product_quantity (
    id BIGSERIAL PRIMARY KEY,
    product_id BIGINT NOT NULL UNIQUE,
    quantity DOUBLE PRECISION NOT NULL,
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
    quantity DOUBLE PRECISION NOT NULL,
    product_unit_id BIGINT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL
);

-- Create DB info table
CREATE TABLE db_info (
    version VARCHAR(20) PRIMARY KEY,
    rack_id VARCHAR(40) NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create debt payment table
CREATE TABLE debt_payment (
    id BIGSERIAL PRIMARY KEY,
    debt_transaction_id BIGINT NOT NULL,
    total_debt MONEY NOT NULL,
    amount_paid MONEY NOT NULL,
    balance MONEY NOT NULL,
    currency VARCHAR(4) NOT NULL,
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
    transaction_table VARCHAR(20) NOT NULL,
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
    client_name VARCHAR(30) NOT NULL,
    client_id BIGINT DEFAULT NULL,
    purpose VARCHAR(100) NOT NULL,
    amount MONEY NOT NULL,
    payment_method PAYMENT_METHOD NOT NULL DEFAULT 'cash',
    currency VARCHAR(4) NOT NULL,
    note_id BIGINT DEFAULT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL
);

-- Create income transaction table
CREATE TABLE income_transaction (
    id BIGSERIAL PRIMARY KEY,
    client_name VARCHAR(30) NOT NULL,
    client_id BIGINT DEFAULT NULL,
    purpose VARCHAR(100) NOT NULL,
    amount MONEY NOT NULL,
    payment_method PAYMENT_METHOD NOT NULL DEFAULT 'cash',
    currency VARCHAR(4) NOT NULL,
    note_id BIGINT DEFAULT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL
);

-- Create initial product quantity table
CREATE TABLE initial_product_quantity (
    id BIGSERIAL PRIMARY KEY,
    product_id BIGINT NOT NULL,
    quantity DOUBLE PRECISION NOT NULL,
    reason VARCHAR(30) NOT NULL,
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
    note VARCHAR(200) NOT NULL,
    table_name VARCHAR(30) DEFAULT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL
);

-- Create product table
CREATE TABLE product (
    id BIGSERIAL PRIMARY KEY,
    product_category_id BIGINT NOT NULL,
    product VARCHAR(200) NOT NULL,
    short_form VARCHAR(10) DEFAULT NULL,
    description VARCHAR(200) DEFAULT NULL,
    barcode VARCHAR(100) DEFAULT NULL,
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
    category VARCHAR(100) NOT NULL UNIQUE,
    short_form VARCHAR(25) DEFAULT NULL,
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
    unit VARCHAR(30) NOT NULL,
    short_form VARCHAR(10) DEFAULT NULL,
    preferred BOOLEAN NOT NULL DEFAULT FALSE,
    base_unit_equivalent DOUBLE PRECISION NOT NULL,
    cost_price MONEY NOT NULL,
    retail_price MONEY NOT NULL,
    currency VARCHAR(4) NOT NULL,
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
    unit_price MONEY NOT NULL,
    quantity DOUBLE PRECISION NOT NULL,
    product_unit_id BIGINT NOT NULL,
    cost MONEY NOT NULL,
    discount MONEY DEFAULT '0.00',
    currency VARCHAR(4) NOT NULL,
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
    amount MONEY NOT NULL,
    payment_method PAYMENT_METHOD NOT NULL DEFAULT 'cash',
    currency VARCHAR(4) NOT NULL,
    note_id BIGINT DEFAULT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL
);

-- Create purchase transaction table
CREATE TABLE purchase_transaction (
    id BIGSERIAL PRIMARY KEY,
    vendor_name VARCHAR(50) NOT NULL,
    vendor_id BIGINT DEFAULT NULL,
    discount MONEY NOT NULL DEFAULT '0.00',
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
    unit_price MONEY NOT NULL,
    quantity DOUBLE PRECISION NOT NULL,
    product_unit_id BIGINT NOT NULL,
    cost MONEY NOT NULL,
    discount MONEY DEFAULT '0.00',
    currency VARCHAR(4) NOT NULL,
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
    amount MONEY NOT NULL,
    payment_method PAYMENT_METHOD NOT NULL DEFAULT 'cash',
    currency VARCHAR(4) NOT NULL,
    note_id BIGINT DEFAULT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL
);

-- Create sale transaction table
CREATE TABLE sale_transaction (
    id BIGSERIAL PRIMARY KEY,
    customer_name VARCHAR(50) NOT NULL,
    customer_id BIGINT DEFAULT NULL,
    discount MONEY NOT NULL DEFAULT '0.00',
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
    old_unit_quantity DOUBLE PRECISION NOT NULL,
    old_unit_id BIGINT NOT NULL,
    new_unit_quantity DOUBLE PRECISION NOT NULL,
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
    username VARCHAR(60) NOT NULL UNIQUE,
    first_name VARCHAR(60) NOT NULL,
    last_name VARCHAR(60) NOT NULL,
    photo BYTEA DEFAULT NULL,
    phone_number VARCHAR(20) DEFAULT NULL,
    email_address VARCHAR(30) DEFAULT NULL,
    active BOOLEAN DEFAULT FALSE,
    note_id BIGINT DEFAULT NULL,
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
