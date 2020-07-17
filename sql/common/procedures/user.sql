CREATE OR REPLACE FUNCTION AddSqlUser (
    IN iUser TEXT,
    IN iPassword TEXT
) RETURNS void
AS $$
BEGIN
    EXECUTE 'CREATE USER ' || iUser || ' WITH PASSWORD ''' || iPassword || '''';
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION AddUser (
    IN iUser TEXT,
    IN iFirstName TEXT,
    IN iLastName TEXT,
    IN iPhoto BYTEA,
    IN iPhoneNumber TEXT,
    IN iEmailAddress TEXT,
    IN iNoteId BIGINT,
    IN iUserId BIGINT
) RETURNS TABLE(user_id BIGINT)
AS $$
DECLARE archived BOOLEAN := NULL;
BEGIN
    EXECUTE 'SELECT archived
            FROM rr_user
            WHERE username = ''' || iUser ||
            ''' AND archived = TRUE' INTO archived;
    IF archived IS NOT NULL THEN
        RAISE EXCEPTION 'This user was previously archived.';
    END IF;

    RETURN QUERY INSERT INTO rr_user (username,
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
                iUserId)
    RETURNING id AS user_id;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION ActivateUser (
    IN iUser TEXT,
    IN iActive BOOLEAN DEFAULT TRUE
) RETURNS void
AS $$
    UPDATE rr_user
        SET active = iActive
        WHERE rr_user.username = iUser;
$$ LANGUAGE sql;

---

CREATE OR REPLACE FUNCTION FetchUserByName (
    iUser TEXT
) RETURNS TABLE(user_id BIGINT, username TEXT, user_privileges JSON)
AS $$
BEGIN
    RETURN QUERY SELECT rr_user.id AS user_id,
        rr_user.username AS username,
        user_privilege.privileges AS user_privileges
    FROM rr_user
    LEFT JOIN user_privilege ON rr_user.id = user_privilege.user_id
    WHERE rr_user.username = iUser;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION ViewUsers (
    iArchived BOOLEAN DEFAULT FALSE
) RETURNS TABLE(user_id BIGINT, username TEXT, active BOOLEAN)
AS $$
BEGIN
    RETURN QUERY SELECT rr_user.id AS user_id,
        rr_user.username AS username,
        rr_user.active AS active
    FROM rr_user
    WHERE archived = iArchived
        AND id > 1;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION FetchUserPrivileges (
    IN iUserId BIGINT
) RETURNS TABLE(user_privileges JSON)
AS $$
BEGIN
    RETURN QUERY SELECT user_privilege.privileges AS user_privileges
        FROM user_privilege
        WHERE user_id = iUserId;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION GrantSqlPrivilege (
    IN iUser TEXT,
    IN iPrivilege TEXT
) RETURNS void
AS $$
BEGIN
    EXECUTE 'GRANT ' || iPrivilege || ' TO ' || iUser;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION RevokeSqlPrivilege (
    IN iUser TEXT,
    IN iPrivilege TEXT
) RETURNS void
AS $$
BEGIN
    EXECUTE 'REVOKE ' || iPrivilege || ' FROM ' || iUser;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION AddUserPrivileges (
    IN iPrivileges JSON,
    IN iUserId BIGINT
) RETURNS TABLE(user_id BIGINT, privileges JSON)
AS $$
BEGIN
    RETURN QUERY INSERT INTO user_privilege (user_id, privileges)
    VALUES (iUserId, iPrivileges)
    RETURNING user_privilege.user_id, user_privilege.privileges;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION UpdateUserPrivileges (
    IN iPrivileges JSON,
    IN iUserId BIGINT
) RETURNS void 
AS $$
    UPDATE user_privilege
        SET privileges = iPrivileges
        WHERE user_id = iUserId;
$$ LANGUAGE sql;

---

CREATE OR REPLACE FUNCTION FetchUser (
    IN iUserId BIGINT,
    IN iArchived BOOLEAN DEFAULT FALSE
) RETURNS TABLE(user_id BIGINT, first_name TEXT, last_name TEXT,
                username TEXT, photo BYTEA, phone_number TEXT,
                email_address TEXT, active BOOLEAN, note TEXT)
AS $$
BEGIN
    RETURN QUERY SELECT rr_user.id AS user_id,
            rr_user.first_name AS first_name,
            rr_user.last_name AS last_name,
            rr_user.username AS username,
            rr_user.photo AS photo,
            rr_user.phone_number AS phone_number,
            rr_user.email_address AS email_address,
            rr_user.active AS active,
            note.note AS note
    FROM rr_user
    LEFT JOIN note ON rr_user.note_id = note.id
    WHERE rr_user.id = iUserId
        AND rr_user.archived = iArchived;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION ChangePassword (
    IN iUser TEXT,
    IN iNewPassword TEXT
) RETURNS void
AS $$
BEGIN
    EXECUTE 'ALTER USER ' || iUser || ' WITH PASSWORD ''$2''' USING iNewPassword;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION RemoveSqlUser (
    iUser TEXT
) RETURNS void
AS $$
BEGIN
    EXECUTE 'DROP USER ' || iUser;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION FetchEmailAddress (
    iUser TEXT
) RETURNS TABLE(user_id BIGINT, email_address TEXT)
AS $$
BEGIN
    RETURN QUERY SELECT rr_user.id AS user_id, rr_user.email_address AS email_address
    FROM rr_user
    WHERE rr_user.username = iUser;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION FetchUserName (
    iEmailAddress TEXT
) RETURNS TABLE(user_id BIGINT, username TEXT)
AS $$
BEGIN
    RETURN QUERY SELECT rr_user.id AS user_id, rr_user.username AS username
    FROM rr_user
    WHERE rr_user.email_address = iEmailAddress;
END
$$ LANGUAGE plpgsql;

---

CREATE OR REPLACE FUNCTION UpdateAdminEmailAddress (
    iEmailAddress TEXT
) RETURNS void
AS $$
    UPDATE rr_user
        SET email_address = iEmailAddress
    WHERE user_id = 1;
$$ LANGUAGE sql;
