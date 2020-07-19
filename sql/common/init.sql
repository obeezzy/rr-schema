--- Create enums
CREATE TYPE PAYMENT_METHOD AS ENUM('cash', 'credit_card', 'debit_card');

-- Create business details table
CREATE TABLE business_details (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    business_family TEXT NOT NULL,
    establishment_year INTEGER NOT NULL CHECK (establishment_year > 0),
    phone_number TEXT DEFAULT NULL,
    logo BYTEA,
    extra_details TEXT DEFAULT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create DB info table
CREATE TABLE db_info (
    version TEXT PRIMARY KEY,
    rack_id TEXT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create note table
CREATE TABLE note (
    id BIGSERIAL PRIMARY KEY,
    note TEXT NOT NULL,
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
    email_address TEXT DEFAULT NULL, active BOOLEAN DEFAULT FALSE,
    note_id BIGINT DEFAULT NULL REFERENCES note(id),
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL DEFAULT 0 REFERENCES rr_user(id)
);

-- Create user privilege table
CREATE TABLE user_privilege (
    user_id BIGINT PRIMARY KEY REFERENCES rr_user(id),
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
    user_id BIGINT NOT NULL REFERENCES rr_user(id)
);

-- Create product category table
CREATE TABLE product_category (
    id BIGSERIAL PRIMARY KEY,
    category TEXT NOT NULL UNIQUE,
    short_form TEXT DEFAULT NULL,
    note_id BIGINT DEFAULT NULL REFERENCES note(id),
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL REFERENCES rr_user(id)
);

-- Create product table
CREATE TABLE product (
    id BIGSERIAL PRIMARY KEY,
    product_category_id BIGINT NOT NULL REFERENCES product_category(id),
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
    user_id BIGINT NOT NULL REFERENCES rr_user(id)
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
    user_id BIGINT NOT NULL REFERENCES rr_user(id)
);

-- Create creditor table
CREATE TABLE creditor (
    id BIGSERIAL PRIMARY KEY,
    client_id BIGINT NOT NULL REFERENCES client(id),
    note_id BIGINT DEFAULT NULL REFERENCES note(id),
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL REFERENCES rr_user(id)
);

-- Create debtor table
CREATE TABLE debtor (
    id BIGSERIAL PRIMARY KEY,
    client_id BIGINT NOT NULL REFERENCES client(id),
    note_id BIGINT DEFAULT NULL REFERENCES note(id),
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL REFERENCES rr_user(id)
);

-- Create vendor table
CREATE TABLE vendor (
    id BIGSERIAL PRIMARY KEY,
    client_id BIGINT NOT NULL UNIQUE REFERENCES client(id),
    note_id BIGINT DEFAULT NULL REFERENCES note(id),
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL REFERENCES rr_user(id)
);

-- Create credit transaction table
CREATE TABLE credit_transaction (
    id BIGSERIAL PRIMARY KEY,
    creditor_id BIGINT NOT NULL REFERENCES creditor(id),
    table_ref TEXT NOT NULL,
    table_id BIGINT DEFAULT NULL,
    note_id BIGINT DEFAULT NULL REFERENCES note(id),
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL REFERENCES rr_user(id)
);

-- Create credit payment table
CREATE TABLE credit_payment (
    id BIGSERIAL PRIMARY KEY,
    credit_transaction_id BIGINT NOT NULL REFERENCES credit_transaction(id),
    total_credit NUMERIC(19,2) NOT NULL CHECK (total_credit > 0),
    amount_paid NUMERIC(19,2) NOT NULL CHECK (amount_paid >= 0),
    balance NUMERIC(19,2) NOT NULL,
    currency VARCHAR(4) NOT NULL,
    due_date_time TIMESTAMP NOT NULL,
    note_id BIGINT DEFAULT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL REFERENCES rr_user(id)
);

-- Create customer table
CREATE TABLE customer (
    id BIGSERIAL PRIMARY KEY,
    client_id BIGINT NOT NULL UNIQUE REFERENCES client(id),
    note_id BIGINT DEFAULT NULL REFERENCES note(id),
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL REFERENCES rr_user(id)
);

-- Create damaged quantity table
CREATE TABLE damaged_quantity (
    id BIGSERIAL PRIMARY KEY,
    product_id BIGINT DEFAULT NULL UNIQUE REFERENCES product(id),
    quantity REAL NOT NULL CHECK (quantity >= 0),
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL REFERENCES rr_user(id)
);

-- Create debt transaction table
CREATE TABLE debt_transaction (
    id BIGSERIAL PRIMARY KEY,
    debtor_id BIGINT NOT NULL REFERENCES debtor(id),
    table_ref TEXT NOT NULL,
    table_id BIGINT DEFAULT NULL,
    note_id BIGINT DEFAULT NULL REFERENCES note(id),
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL REFERENCES rr_user(id)
);

-- Create debt payment table
CREATE TABLE debt_payment (
    id BIGSERIAL PRIMARY KEY,
    debt_transaction_id BIGINT NOT NULL REFERENCES debt_transaction(id),
    total_debt NUMERIC(19,2) NOT NULL CHECK (total_debt > 0),
    amount_paid NUMERIC(19,2) NOT NULL CHECK (amount_paid >= 0),
    balance NUMERIC(19,2) NOT NULL,
    currency VARCHAR(4) NOT NULL,
    due_date_time TIMESTAMP NOT NULL,
    note_id BIGINT DEFAULT NULL REFERENCES note(id),
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL REFERENCES rr_user(id)
);

-- Create expense transaction table
CREATE TABLE expense_transaction (
    id BIGSERIAL PRIMARY KEY,
    client_name TEXT NOT NULL,
    client_id BIGINT DEFAULT NULL REFERENCES client(id),
    purpose TEXT NOT NULL,
    amount NUMERIC(19,2) NOT NULL,
    payment_method PAYMENT_METHOD NOT NULL DEFAULT 'cash',
    currency VARCHAR(4) NOT NULL,
    note_id BIGINT DEFAULT NULL REFERENCES note(id),
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL REFERENCES rr_user(id)
);

-- Create income transaction table
CREATE TABLE income_transaction (
    id BIGSERIAL PRIMARY KEY,
    client_name TEXT NOT NULL,
    client_id BIGINT DEFAULT NULL REFERENCES client(id),
    purpose TEXT NOT NULL,
    amount NUMERIC(19,2) NOT NULL,
    payment_method PAYMENT_METHOD NOT NULL DEFAULT 'cash',
    currency VARCHAR(4) NOT NULL,
    note_id BIGINT DEFAULT NULL REFERENCES note(id),
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL REFERENCES rr_user(id)
);

-- Create product quantity table
CREATE TABLE product_quantity (
    id BIGSERIAL PRIMARY KEY,
    product_id BIGINT NOT NULL UNIQUE REFERENCES product(id),
    quantity REAL NOT NULL CHECK (quantity >= 0),
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL REFERENCES rr_user(id)
);

-- Create product quantity snapshot table
CREATE TABLE product_quantity_snapshot (
    id BIGSERIAL PRIMARY KEY,
    product_id BIGINT NOT NULL REFERENCES product(id),
    quantity REAL NOT NULL CHECK (quantity >= 0),
    reason TEXT NOT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL REFERENCES rr_user(id)
);

-- Create product unit table
CREATE TABLE product_unit (
    id BIGSERIAL PRIMARY KEY,
    product_id BIGINT NOT NULL REFERENCES product(id),
    unit TEXT NOT NULL,
    short_form TEXT DEFAULT NULL,
    preferred BOOLEAN NOT NULL DEFAULT FALSE,
    base_unit_equivalent REAL NOT NULL,
    cost_price NUMERIC(19,2) NOT NULL,
    retail_price NUMERIC(19,2) NOT NULL,
    currency VARCHAR(4) NOT NULL,
    note_id BIGINT DEFAULT NULL REFERENCES note(id),
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL REFERENCES rr_user(id)
);

-- Create purchase transaction table
CREATE TABLE purchase_transaction (
    id BIGSERIAL PRIMARY KEY,
    vendor_name TEXT NOT NULL,
    vendor_id BIGINT DEFAULT NULL REFERENCES vendor(id),
    discount NUMERIC(19,2) NOT NULL DEFAULT '0.00' CHECK (discount >= 0),
    suspended BOOLEAN NOT NULL DEFAULT FALSE,
    note_id BIGINT DEFAULT NULL REFERENCES note(id),
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL REFERENCES rr_user(id)
);

-- Create purchase payment table
CREATE TABLE purchase_payment (
    id BIGSERIAL PRIMARY KEY,
    purchase_transaction_id BIGINT NOT NULL REFERENCES purchase_transaction(id),
    amount NUMERIC(19,2) NOT NULL CHECK (amount >= 0),
    payment_method PAYMENT_METHOD NOT NULL DEFAULT 'cash',
    currency VARCHAR(4) NOT NULL,
    note_id BIGINT DEFAULT NULL REFERENCES note(id),
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL REFERENCES rr_user(id)
);

-- Create purchased product table
CREATE TABLE purchased_product (
    id BIGSERIAL PRIMARY KEY,
    purchase_transaction_id BIGINT NOT NULL REFERENCES purchase_transaction(id),
    product_id BIGINT NOT NULL REFERENCES product(id),
    unit_price NUMERIC(19,2) NOT NULL CHECK (unit_price >= 0),
    quantity REAL NOT NULL CHECK (quantity > 0),
    product_unit_id BIGINT NOT NULL REFERENCES product_unit(id),
    cost NUMERIC(19,2) NOT NULL,
    discount NUMERIC(19,2) DEFAULT '0.00',
    currency VARCHAR(4) NOT NULL,
    note_id BIGINT DEFAULT NULL REFERENCES note(id),
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL REFERENCES rr_user(id)
);

-- Create sale transaction table
CREATE TABLE sale_transaction (
    id BIGSERIAL PRIMARY KEY,
    customer_name TEXT NOT NULL,
    customer_id BIGINT DEFAULT NULL REFERENCES customer(id),
    discount NUMERIC(19,2) NOT NULL DEFAULT '0.00' CHECK (discount >= 0),
    suspended BOOLEAN NOT NULL DEFAULT FALSE,
    note_id BIGINT DEFAULT NULL REFERENCES note(id),
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL REFERENCES rr_user(id)
);

-- Create sale payment table
CREATE TABLE sale_payment (
    id BIGSERIAL PRIMARY KEY,
    sale_transaction_id BIGINT NOT NULL REFERENCES sale_transaction(id),
    amount NUMERIC(19,2) NOT NULL CHECK (amount > 0),
    payment_method PAYMENT_METHOD NOT NULL DEFAULT 'cash',
    currency VARCHAR(4) NOT NULL,
    note_id BIGINT DEFAULT NULL REFERENCES note(id),
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL REFERENCES rr_user(id)
);

-- Create sold product table
CREATE TABLE sold_product (
    id BIGSERIAL PRIMARY KEY,
    sale_transaction_id BIGINT NOT NULL REFERENCES sale_transaction(id),
    product_id BIGINT NOT NULL REFERENCES product(id),
    unit_price NUMERIC(19,2) NOT NULL CHECK (unit_price >= 0),
    quantity REAL NOT NULL CHECK (quantity > 0),
    product_unit_id BIGINT NOT NULL REFERENCES product_unit(id),
    cost NUMERIC(19,2) NOT NULL CHECK (cost >= 0),
    discount NUMERIC(19,2) DEFAULT '0.00' CHECK (discount >= 0),
    currency VARCHAR(4) NOT NULL,
    note_id BIGINT DEFAULT NULL REFERENCES note(id),
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL REFERENCES rr_user(id)
);

-- Create unit relation table
CREATE TABLE unit_relation (
    id BIGSERIAL PRIMARY KEY,
    product_id BIGINT NOT NULL REFERENCES product(id),
    old_unit_quantity REAL NOT NULL CHECK (old_unit_quantity >= 0),
    old_unit_id BIGINT NOT NULL REFERENCES product_unit(id),
    new_unit_quantity REAL NOT NULL CHECK (new_unit_quantity >= 0),
    new_unit_id BIGINT NOT NULL REFERENCES product_unit(id),
    note_id BIGINT NOT NULL DEFAULT 0 REFERENCES note(id),
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL REFERENCES rr_user(id)
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
