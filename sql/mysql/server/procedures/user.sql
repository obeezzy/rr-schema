USE ###DATABASENAME###;

---

DROP PROCEDURE IF EXISTS AddSqlUser;
---
CREATE PROCEDURE AddSqlUser (
    IN iUser VARCHAR(100),
    IN iPassword VARCHAR(100)
)
BEGIN
    DECLARE _HOST CHAR(14) DEFAULT '@\'localhost\'';
    SET iUser := CONCAT('\'', REPLACE(TRIM(iUser), CHAR(39), CONCAT(CHAR(92), CHAR(39))), '\''),
        iPassword := CONCAT('\'', REPLACE(iPassword, CHAR(39), CONCAT(CHAR(92), CHAR(39))), '\'');
    SET @sql := CONCAT('CREATE USER ', iUser, _HOST, ' IDENTIFIED BY ', iPassword);
    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    SET @sql := CONCAT('GRANT ALL PRIVILEGES ON *.* TO ', iUser, _HOST);
    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
    FLUSH PRIVILEGES;
END;

---

DROP PROCEDURE IF EXISTS GrantSqlPrivilege;
---
CREATE PROCEDURE GrantSqlPrivilege (
    IN iUser VARCHAR(50),
    IN iPrivilege VARCHAR(30)
)
BEGIN
    DECLARE _HOST CHAR(14) DEFAULT '@\'localhost\'';
    SET iUser := CONCAT('\'', REPLACE(TRIM(iUser), CHAR(39), CONCAT(CHAR(92), CHAR(39))), '\'');
    SET @sql := CONCAT('GRANT ', iPrivilege, ' ON *.* TO ', iUser, _HOST);
    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
    FLUSH PRIVILEGES;
END;