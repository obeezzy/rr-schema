USE mysql;

-- Create database
DROP DATABASE IF EXISTS ###DATABASENAME###;
CREATE DATABASE ###DATABASENAME###;

USE ###DATABASENAME###;

-- Create business details table
CREATE TABLE business_details (
    id INTEGER NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(200) NOT NULL,
    business_family VARCHAR(500) NOT NULL,
    establishment_year INTEGER NOT NULL,
    phone_number VARCHAR(20) DEFAULT NULL,
    logo BLOB,
    extra_details VARCHAR(100) DEFAULT NULL,
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Create client table
CREATE TABLE client (
    id INTEGER NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(100) DEFAULT NULL,
    last_name VARCHAR(100) DEFAULT NULL,
    preferred_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    alternate_phone_number VARCHAR(20) DEFAULT NULL,
    address VARCHAR(100) DEFAULT NULL,
    note_id INTEGER DEFAULT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY phone_number (phone_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Create credit payment table
CREATE TABLE credit_payment (
    id INTEGER NOT NULL AUTO_INCREMENT,
    credit_transaction_id INTEGER NOT NULL,
    total_credit DECIMAL(19,2) NOT NULL,
    amount_paid DECIMAL(19,2) NOT NULL,
    balance DECIMAL(19,2) NOT NULL,
    currency VARCHAR(4) NOT NULL,
    due_date_time DATETIME NOT NULL,
    note_id INTEGER DEFAULT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Create creditor table
CREATE TABLE creditor (
    id INTEGER NOT NULL AUTO_INCREMENT,
    client_id INTEGER NOT NULL,
    note_id INTEGER DEFAULT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Create credit transaction table
CREATE TABLE credit_transaction (
    id INTEGER NOT NULL AUTO_INCREMENT,
    creditor_id INTEGER NOT NULL,
    transaction_table VARCHAR(20) NOT NULL,
    transaction_id INTEGER DEFAULT NULL,
    note_id INTEGER DEFAULT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Create current product quantity table
CREATE TABLE current_product_quantity (
    id INTEGER NOT NULL AUTO_INCREMENT,
    product_id INTEGER DEFAULT NULL,
    quantity DOUBLE NOT NULL,
    product_unit_id INTEGER NOT NULL,
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY product_id (product_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Create customer table
CREATE TABLE customer (
    id INTEGER NOT NULL AUTO_INCREMENT,
    client_id INTEGER NOT NULL,
    note_id INTEGER DEFAULT NULL,
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY client_id (client_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Create damaged quantity table
CREATE TABLE damaged_quantity (
    id INTEGER NOT NULL AUTO_INCREMENT,
    product_id INTEGER DEFAULT NULL,
    quantity DOUBLE NOT NULL,
    product_unit_id INTEGER NOT NULL,
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY product_id (product_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Create DB info table
CREATE TABLE db_info (
    version VARCHAR(20) NOT NULL,
    rack_id VARCHAR(40) NOT NULL,
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (version)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Create debt payment table
CREATE TABLE debt_payment (
    id INTEGER NOT NULL AUTO_INCREMENT,
    debt_transaction_id INTEGER NOT NULL,
    total_debt DECIMAL(19,2) NOT NULL,
    amount_paid DECIMAL(19,2) NOT NULL,
    balance DECIMAL(19,2) NOT NULL,
    currency VARCHAR(4) NOT NULL,
    due_date_time DATETIME NOT NULL,
    note_id INTEGER DEFAULT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Create debt transaction table
CREATE TABLE debt_transaction (
    id INTEGER NOT NULL AUTO_INCREMENT,
    debtor_id INTEGER NOT NULL,
    transaction_table VARCHAR(20) NOT NULL,
    transaction_id INTEGER DEFAULT NULL,
    note_id INTEGER DEFAULT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Create debtor table
CREATE TABLE debtor (
    id INTEGER NOT NULL AUTO_INCREMENT,
    client_id INTEGER NOT NULL,
    note_id INTEGER DEFAULT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Create expense transaction table
CREATE TABLE expense_transaction (
    id INTEGER NOT NULL AUTO_INCREMENT,
    client_name VARCHAR(30) NOT NULL,
    client_id INTEGER DEFAULT NULL,
    purpose VARCHAR(100) NOT NULL,
    amount DECIMAL(19,2) NOT NULL,
    payment_method ENUM('cash', 'credit_card', 'debit_card') NOT NULL DEFAULT 'cash',
    currency VARCHAR(4) NOT NULL,
    note_id INTEGER DEFAULT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Create income transaction table
CREATE TABLE income_transaction (
    id INTEGER NOT NULL AUTO_INCREMENT,
    client_name VARCHAR(30) NOT NULL,
    client_id INTEGER DEFAULT NULL,
    purpose VARCHAR(100) NOT NULL,
    amount DECIMAL(19,2) NOT NULL,
    payment_method ENUM('cash', 'credit_card', 'debit_card') NOT NULL DEFAULT 'cash',
    currency VARCHAR(4) NOT NULL,
    note_id INTEGER DEFAULT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Create initial product quantity table
CREATE TABLE initial_product_quantity (
    id INTEGER NOT NULL AUTO_INCREMENT,
    product_id INTEGER NOT NULL,
    quantity DOUBLE NOT NULL,
    product_unit_id INTEGER NOT NULL,
    reason VARCHAR(30) NOT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Create last used date/time table
CREATE TABLE last_used_date_time (
    last_date_time DATETIME NOT NULL,
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (last_date_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Create note table
CREATE TABLE note (
    id INTEGER NOT NULL AUTO_INCREMENT,
    note VARCHAR(200) NOT NULL,
    table_name VARCHAR(30) DEFAULT NULL,
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Create product table
CREATE TABLE product (
    id INTEGER NOT NULL AUTO_INCREMENT,
    product_category_id INTEGER NOT NULL,
    product VARCHAR(200) NOT NULL,
    short_form VARCHAR(10) DEFAULT NULL,
    description VARCHAR(200) DEFAULT NULL,
    barcode VARCHAR(70) DEFAULT NULL,
    divisible BOOLEAN DEFAULT 1,
    image BLOB,
    note_id INTEGER DEFAULT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY barcode (barcode)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Create product category table
CREATE TABLE product_category (
    id INTEGER NOT NULL AUTO_INCREMENT,
    category VARCHAR(100) NOT NULL,
    short_form VARCHAR(25) DEFAULT NULL,
    note_id INTEGER DEFAULT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY category (category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Create product_unit tale
CREATE TABLE product_unit (
    id INTEGER NOT NULL AUTO_INCREMENT,
    product_id INTEGER NOT NULL,
    unit VARCHAR(30) NOT NULL,
    short_form VARCHAR(10) DEFAULT NULL,
    preferred BOOLEAN NOT NULL DEFAULT FALSE,
    base_unit_equivalent INTEGER NOT NULL,
    cost_price DECIMAL(19,2) NOT NULL,
    retail_price DECIMAL(19,2) NOT NULL,
    currency VARCHAR(4) NOT NULL,
    note_id INTEGER DEFAULT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Create purchased product table
CREATE TABLE purchased_product (
    id INTEGER NOT NULL AUTO_INCREMENT,
    purchase_transaction_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    unit_price DECIMAL(19,2) NOT NULL,
    quantity DOUBLE NOT NULL,
    product_unit_id INTEGER NOT NULL,
    cost DECIMAL(19,2) NOT NULL,
    discount DECIMAL(19,2) DEFAULT '0.00',
    currency VARCHAR(4) NOT NULL,
    note_id INTEGER DEFAULT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Create purchase payment table
CREATE TABLE purchase_payment (
    id INTEGER NOT NULL AUTO_INCREMENT,
    purchase_transaction_id INTEGER NOT NULL,
    amount DECIMAL(19,2) NOT NULL,
    payment_method ENUM('cash', 'credit_card', 'debit_card') NOT NULL DEFAULT 'cash',
    currency VARCHAR(4) NOT NULL,
    note_id INTEGER DEFAULT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Create purchase transaction table
CREATE TABLE purchase_transaction (
    id INTEGER NOT NULL AUTO_INCREMENT,
    vendor_name VARCHAR(50) NOT NULL,
    vendor_id INTEGER DEFAULT NULL,
    discount DECIMAL(19,2) NOT NULL DEFAULT '0.00',
    suspended BOOLEAN NOT NULL DEFAULT FALSE,
    note_id INTEGER DEFAULT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Create sold product table
CREATE TABLE sold_product (
    id INTEGER NOT NULL AUTO_INCREMENT,
    sale_transaction_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    unit_price DECIMAL(19,2) NOT NULL,
    quantity DOUBLE NOT NULL,
    product_unit_id INTEGER NOT NULL,
    cost DECIMAL(19,2) NOT NULL,
    discount DECIMAL(19,2) DEFAULT '0.00',
    currency VARCHAR(4) NOT NULL,
    note_id INTEGER DEFAULT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Create sale payment table
CREATE TABLE sale_payment (
    id INTEGER NOT NULL AUTO_INCREMENT,
    sale_transaction_id INTEGER NOT NULL,
    amount DECIMAL(19,2) NOT NULL,
    payment_method ENUM('cash', 'credit_card', 'debit_card') NOT NULL,
    currency VARCHAR(4) NOT NULL,
    note_id INTEGER DEFAULT NULL,
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Create sale transaction table
CREATE TABLE sale_transaction (
    id INTEGER NOT NULL AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    client_id INTEGER DEFAULT NULL,
    discount DECIMAL(19,2) NOT NULL,
    suspended BOOLEAN NOT NULL,
    note_id INTEGER DEFAULT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Create unit relation table
CREATE TABLE unit_relation (
    id INTEGER NOT NULL AUTO_INCREMENT,
    product_id INTEGER NOT NULL,
    old_unit_quantity DOUBLE NOT NULL,
    old_unit_id INTEGER NOT NULL,
    new_unit_quantity DOUBLE NOT NULL,
    new_unit_id INTEGER NOT NULL,
    note_id INTEGER NOT NULL DEFAULT 0,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Create user table
CREATE TABLE rr_user (
    id INTEGER NOT NULL AUTO_INCREMENT,
    user VARCHAR(60) NOT NULL,
    first_name VARCHAR(60) NOT NULL,
    last_name VARCHAR(60) NOT NULL,
    photo BLOB DEFAULT NULL,
    phone_number VARCHAR(20) DEFAULT NULL,
    email_address VARCHAR(30) DEFAULT NULL,
    active BOOLEAN DEFAULT 0,
    note_id INTEGER DEFAULT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (id),
    UNIQUE user (user)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Create user privilege table
CREATE TABLE user_privilege (
    user_id INTEGER NOT NULL,
    privileges JSON NOT NULL,
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Create user privilege preset table
CREATE TABLE user_privilege_preset (
    id INTEGER NOT NULL AUTO_INCREMENT,
    preset JSON NOT NULL,
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Create vendor table
CREATE TABLE vendor (
    id INTEGER NOT NULL AUTO_INCREMENT,
    client_id INTEGER NOT NULL,
    note_id INTEGER DEFAULT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_edited DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    PRIMARY KEY (id),
    UNIQUE client_id (client_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Add admin user
INSERT INTO rr_user (user,
                    first_name,
                    last_name,
                    active,
                    user_id)
    VALUES ('admin',
            'admin',
            'admin',
            TRUE,
            1);
