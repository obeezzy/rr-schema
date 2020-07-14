CREATE OR REPLACE FUNCTION UpdateBusinessDetails (
    IN iName VARCHAR(100),
    IN iAddress VARCHAR(100),
    IN iBusinessFamily VARCHAR(10),
    IN iEstablishmentYear INTEGER,
    IN iPhoneNumber VARCHAR(20),
    IN iLogo BYTEA,
    IN iExtraDetails VARCHAR(200)
) RETURNS void
AS $$
BEGIN
    INSERT INTO business_details (id,
                                    name,
                                    address,
                                    business_family,
                                    establishment_year,
                                    phone_number,
                                    logo,
                                    extra_details)
        VALUES (1,
                iName,
                iAddress,
                iBusinessFamily,
                iEstablishmentYear,
                iPhoneNumber,
                iLogo,
                iExtraDetails)
        ON CONFLICT (id) DO UPDATE
            SET name = iName,
                address = iAddress,
                business_family = iBusinessFamily,
                establishment_year = iEstablishmentYear,
                phone_number = iPhoneNumber,
                logo = iLogo,
                extra_details = iExtraDetails;
END
$$ LANGUAGE plpgsql;
