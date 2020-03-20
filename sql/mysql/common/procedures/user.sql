USE ###DATABASENAME###;

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

CREATE PROCEDURE AddRRUser (
    IN iUser VARCHAR(100),
    IN iFirstName VARCHAR(100),
    IN iLastName VARCHAR(100),
    IN iPhoto BLOB,
    IN iPhoneNumber VARCHAR(100),
    IN iEmailAddress VARCHAR(100),
    IN iNoteId INTEGER,
    IN iUserId INTEGER
)
BEGIN
    SET @archived := NULL;
    SELECT archived INTO @archived
        FROM rr_user
        WHERE user = iUser
        AND archived = TRUE;
    IF @archived IS NOT NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'This user was previously archived.';
    END IF;

    INSERT INTO rr_user (user,
                        first_name,
                        last_name,
                        photo,
                        phone_number,
                        email_address,
                        note_id,
                        user_id)
        VALUES (iUser,
                iFirstName,
                iLastName,
                iPhoto,
                iPhoneNumber,
                iEmailAddress,
                NULLIF(iNoteId, 0),
                iUserId);
    SELECT LAST_INSERT_ID() AS user_id;
END;

---

CREATE PROCEDURE ActivateUser (
    IN iUser VARCHAR(50),
    IN iActive BOOLEAN
)
BEGIN
    DECLARE _HOST CHAR(14) DEFAULT '@\'localhost\'';
    UPDATE rr_user
        SET active = IFNULL(iActive, FALSE)
        WHERE rr_user.user = iUser;
    SET iUser := CONCAT('\'', REPLACE(TRIM(iUser), CHAR(39), CONCAT(CHAR(92), CHAR(39))), '\'');

    SET @sql := NULL;
    IF iActive = TRUE THEN
        SET @sql := CONCAT('ALTER USER ', iUser, _HOST, ' ACCOUNT UNLOCK');
    ELSE
        SET @sql := CONCAT('ALTER USER ', iUser, _HOST, ' ACCOUNT LOCK');
    END IF;

    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
    FLUSH PRIVILEGES;
END

---

CREATE PROCEDURE FetchUserByName (
	iUser VARCHAR(50)
)
BEGIN
	SELECT rr_user.id AS user_id,
            rr_user.user AS user,
            user_privilege.privileges AS user_privileges
        FROM rr_user
		LEFT JOIN user_privilege ON rr_user.id = user_privilege.user_id
        WHERE user = iUser;
END

---

CREATE PROCEDURE ViewUsers (
    iArchived BOOLEAN
)
BEGIN
	SELECT id AS user_id, user, active
        FROM rr_user
        WHERE archived = IFNULL(iArchived, FALSE)
        AND id > 1;
END;

---

CREATE PROCEDURE FetchUserPrivileges (
	IN iUserId INTEGER
)
BEGIN
	SELECT privileges AS user_privileges
        FROM user_privilege
        WHERE user_id = iUserId;
END;

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

---

CREATE PROCEDURE RevokeSqlPrivilege (
    IN iUser VARCHAR(50),
    IN iPrivilege VARCHAR(30)
)
BEGIN
    DECLARE _HOST CHAR(14) DEFAULT '@\'localhost\'';
    SET iUser := CONCAT('\'', REPLACE(TRIM(iUser), CHAR(39), CONCAT(CHAR(92), CHAR(39))), '\'');
    SET @sql := CONCAT('REVOKE ', iPrivilege, ' ON *.* TO ', iUser, _HOST);
    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
    FLUSH PRIVILEGES;
END;

---

CREATE PROCEDURE AddUserPrivileges (
    IN iPrivileges JSON,
    IN iUserId INTEGER
)
BEGIN
    INSERT INTO user_privilege (user_id,
                                privileges,
                                created,
                                last_edited)
        VALUES (iUserId,
                iPrivileges,
                CURRENT_TIMESTAMP(),
                CURRENT_TIMESTAMP());
END;

---

CREATE PROCEDURE UpdateUserPrivileges (
    IN iPrivileges JSON,
    IN iUserId INTEGER
)
BEGIN
    UPDATE user_privilege
        SET privileges = iPrivileges
        WHERE user_id = iUserId;
END;

---

CREATE PROCEDURE FetchUser (
    IN iUserId INTEGER,
    IN iArchived BOOLEAN
)
BEGIN
    SELECT rr_user.id AS user_id,
            rr_user.first_name AS first_name,
            rr_user.last_name AS last_name,
            rr_user.user AS user,
            rr_user.photo AS photo,
            rr_user.phone_number AS phone_number,
            rr_user.email_address AS email_address,
            rr_user.active AS active,
            note.note AS note
        FROM rr_user
        LEFT JOIN note ON rr_user.note_id = note.id
        WHERE rr_user.id = iUserId
        AND rr_user.archived = IFNULL(iArchived, FALSE);
END;

---

CREATE PROCEDURE ChangePassword (
    IN iUser VARCHAR(100),
    IN iNewPassword VARCHAR(256)
)
BEGIN
    DECLARE _HOST CHAR(14) DEFAULT '@\'localhost\'';

	SET iUser := CONCAT('\'', REPLACE(TRIM(iUser), CHAR(39), CONCAT(CHAR(92), CHAR(39))), '\''),
        iNewPassword := CONCAT('\'', REPLACE(iNewPassword, CHAR(39), CONCAT(CHAR(92), CHAR(39))), '\'');
    SET @sql := CONCAT('ALTER USER ', iUser, _HOST, ' IDENTIFIED BY ', iNewPassword);
    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
    FLUSH PRIVILEGES;
END;

---

CREATE PROCEDURE RemoveUser (
    iUser VARCHAR(40)
)
BEGIN
    DECLARE _HOST CHAR(14) DEFAULT '@\'localhost\'';

    UPDATE rr_user
        SET archived = TRUE
        WHERE rr_user.user = iUser;

	SET iUser := CONCAT('\'', REPLACE(TRIM(iUser), CHAR(39), CONCAT(CHAR(92), CHAR(39))), '\'');
    SET @sql := CONCAT('DROP USER ', iUser, _HOST);
    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
    FLUSH PRIVILEGES;
END;

---

CREATE PROCEDURE FetchEmailAddress (
    iUserName VARCHAR(40)
)
BEGIN
    SELECT id, email_address
        FROM rr_user
        WHERE user = iUserName;
END;

---

CREATE PROCEDURE FetchUserName (
    iEmailAddress VARCHAR(40)
)
BEGIN
    SELECT id AS user_id,
            user
        FROM rr_user
        WHERE email_address = iEmailAddress;
END;

---

CREATE PROCEDURE UpdateAdminEmailAddress (
    iEmailAddress VARCHAR(100)
)
BEGIN
    UPDATE rr_user
        SET email_address = iEmailAddress
        WHERE user = 'admin';
END;