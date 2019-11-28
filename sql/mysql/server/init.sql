CREATE DATABASE IF NOT EXISTS `rr_server`;

USE `rr_server`;

-- Create business admin table
CREATE TABLE IF NOT EXISTS `business_admin` (
    id INT(11) NOT NULL AUTO_INCREMENT,
    email_address VARCHAR(200) NOT NULL UNIQUE,
    first_name VARCHAR(200) NOT NULL,
    last_name VARCHAR(200) NOT NULL,
    phone_number VARCHAR(20),
    photo BLOB,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created DATETIME NOT NULL,
    last_edited DATETIME NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Create business store table
CREATE TABLE IF NOT EXISTS `business_store` (
    id INT(11) NOT NULL AUTO_INCREMENT,
    business_admin_id INT(11) NOT NULL,
    name VARCHAR(300) NOT NULL,
    rack_id VARCHAR(20) NOT NULL UNIQUE,
    address VARCHAR(200) NOT NULL,
    location POINT SRID 4326,
    business_family VARCHAR(50) NOT NULL,
    establishment_year INT(11) DEFAULT NULL,
    phone_number VARCHAR(20) DEFAULT NULL,
    logo BLOB,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created DATETIME NOT NULL,
    last_edited DATETIME NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;