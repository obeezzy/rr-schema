CREATE OR REPLACE FUNCTION AddSqlUser (
    IN iUser VARCHAR(100),
    IN iPassword VARCHAR(100)
)
AS $$
BEGIN
    EXECUTE 'CREATE USER ' || iUser || ' WITH PASSWORD ''' || iPassword || '''';
END
$$ LANGUAGE plpgsql;

---

CREATE PROCEDURE GrantSqlPrivilege (
    IN iUser VARCHAR(50),
    IN iPrivilege VARCHAR(30)
) RETURNS void
AS $$
BEGIN
    EXECUTE 'GRANT ' || iPrivilege || ' TO ' || iUser;
END
$$ LANGUAGE plpgsql;
