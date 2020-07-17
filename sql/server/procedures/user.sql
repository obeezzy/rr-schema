CREATE OR REPLACE FUNCTION AddSqlUser (
    IN iUser TEXT,
    IN iPassword TEXT
)
AS $$
BEGIN
    EXECUTE 'CREATE USER ' || iUser || ' WITH PASSWORD ''' || iPassword || '''';
END
$$ LANGUAGE plpgsql;

---

CREATE PROCEDURE GrantSqlPrivilege (
    IN iUser TEXT,
    IN iPrivilege TEXT
) RETURNS void
AS $$
BEGIN
    EXECUTE 'GRANT ' || iPrivilege || ' TO ' || iUser;
END
$$ LANGUAGE plpgsql;
