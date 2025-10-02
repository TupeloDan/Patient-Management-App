DROP PROCEDURE IF EXISTS sp_MovePerson;

CREATE PROCEDURE sp_MovePerson(
    IN p_current_id INT,
    IN p_nhi VARCHAR(255),
    IN p_name VARCHAR(255),
    IN p_legal_id INT,
    IN p_has_vnr BOOLEAN,
    IN p_treatment_plans_due DATETIME,
    IN p_honos_due DATETIME,
    IN p_uds_due DATETIME,
    IN p_rel_security BOOLEAN,
    IN p_profile BOOLEAN,
    IN p_metobolic BOOLEAN,
    IN p_bloods BOOLEAN,
    IN p_flight_risk BOOLEAN,
    IN p_uds_frequency VARCHAR(255),
    IN p_mdt_day VARCHAR(255),
    IN p_clinician_id INT,
    IN p_cm_id INT,
    IN p_cm_2nd_id INT,
    IN p_assoc_id INT,
    IN p_assoc_2nd_id INT,
    IN p_progress_percent DOUBLE,
    IN p_special_notes TEXT,
    IN p_is_special_patient BOOLEAN,
    IN p_last_treatment_plan DATETIME,
    IN p_last_honos DATETIME,
    IN p_last_uds DATETIME,
    IN p_destination_room VARCHAR(255),
    OUT p_new_id INT
)
BEGIN
    -- Step 1: Create a new record in the destination room with all the data
    INSERT INTO People (
        Room, NHI, PersonName, LegalStatusID, HasVNR, TreatmentPlans, HoNos, UDSDue,
        RelSecurity, `Profile`, Metobolic, Bloods, FlightRisk, UDSFrequency, MDTDay,
        ClinicianID, CaseManagerID, CaseManager2ndID, AssociateID, Associate2ndID,
        `Progress%`, SpecialNotes, IsSpecialPatient, LastTreatmentPlan, LastHonos, LastUDS
    )
    VALUES (
        p_destination_room, p_nhi, p_name, p_legal_id, p_has_vnr, p_treatment_plans_due, p_honos_due, p_uds_due,
        p_rel_security, p_profile, p_metobolic, p_bloods, p_flight_risk, p_uds_frequency, p_mdt_day,
        p_clinician_id, p_cm_id, p_cm_2nd_id, p_assoc_id, p_assoc_2nd_id,
        p_progress_percent, p_special_notes, p_is_special_patient, p_last_treatment_plan, p_last_honos, p_last_uds
    );

    -- Step 2: Get the ID of the newly created record
    SET p_new_id = LAST_INSERT_ID();

    -- Step 3: Clear the old record from the original room
    UPDATE People
    SET NHI = NULL, PersonName = NULL, LegalStatusID = NULL, HasVNR = 0,
        TreatmentPlans = NULL, HoNos = NULL, UDSDue = NULL, RelSecurity = 0,
        `Profile` = 0, Metobolic = 0, Bloods = 0, FlightRisk = 0,
        UDSFrequency = NULL, MDTDay = NULL, ClinicianID = NULL, CaseManagerID = NULL,
        CaseManager2ndID = NULL, AssociateID = NULL, Associate2ndID = NULL, `Progress%` = 0,
        SpecialNotes = NULL, IsSpecialPatient = 0, LastTreatmentPlan = NULL,
        LastHonos = NULL, LastUDS = NULL, LeaveReturn = NULL
    WHERE ID = p_current_id;

END;