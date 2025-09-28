DROP PROCEDURE IF EXISTS sp_AddLeave;

CREATE PROCEDURE sp_AddLeave(
    IN p_nhi VARCHAR(255),
    IN p_patient_name VARCHAR(255),
    IN p_leave_date DATE,
    IN p_leave_time DATETIME, -- CORRECTED: Changed from TIME to DATETIME
    IN p_expected_return_time DATETIME,
    IN p_leave_type VARCHAR(255),
    IN p_is_escorted_leave BOOLEAN,
    IN p_staff_responsible_id INT,
    IN p_leave_description TEXT,
    IN p_mse_completed BOOLEAN,
    IN p_risk_assessment_completed BOOLEAN,
    IN p_leave_conditions_met BOOLEAN,
    IN p_awol_aware BOOLEAN,
    IN p_contact_aware BOOLEAN,
    IN p_senior_notified BOOLEAN,
    OUT p_new_id INT
)
BEGIN
    INSERT INTO LeaveLog (
        NHI, Name, LeaveDate, LeaveTime, ExpectedReturnTime, LeaveType, 
        `Is Escorted`, StaffResponsibleID, LeaveDescription, MSE, Risk, 
        LeaveCondition, AWOL, HasContactInfo, SeniorNurseNotified
    )
    VALUES (
        p_nhi, p_patient_name, p_leave_date, p_leave_time, p_expected_return_time, p_leave_type, 
        p_is_escorted_leave, p_staff_responsible_id, p_leave_description, p_mse_completed, p_risk_assessment_completed,
        p_leave_conditions_met, p_awol_aware, p_contact_aware, p_senior_notified
    );

    SET p_new_id = LAST_INSERT_ID();
END