document.addEventListener('DOMContentLoaded', () => {
    // --- Initializations ---
    const datePicker = flatpickr("#modal-date-input", { dateFormat: "d/m/Y" });
    const staffResponsibleChoice = new Choices('#staff-responsible-select', { removeItemButton: true, searchResultLimit: 10 });
    const staffMseChoice = new Choices('#staff-mse-select', { removeItemButton: true, searchResultLimit: 10 });
    const shiftLeadChoice = new Choices('#shift-lead-select', { removeItemButton: true, searchResultLimit: 10 });

    // --- API Endpoints & Config ---
    const PATIENTS_API = '/api/people';
    const STAFF_API = '/api/staff';
    const DELEGATED_STAFF_API = '/api/delegated-staff';
    const UI_TEXT_API = '/api/ui-text';
    const LEAVES_API = '/api/leaves';
    const UDS_OPTIONS = ['Weekly', 'Bi-Weekly', 'Monthly', 'Random', 'OnRequest'];
    const MDT_DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];

    // --- DOM Elements ---
    const patientListContainer = document.getElementById('patient-list-container');
    const detailsPane = document.getElementById('details-pane');
    const detailsHeader = document.getElementById('details-header');
    const addLeaveModal = document.getElementById('add-leave-modal');
    const addLeaveTitle = document.getElementById('add-leave-title');
    const escortedChecklistContainer = document.getElementById('escorted-checklist-container');
    const unescortedChecklistContainer = document.getElementById('unescorted-checklist-container');
    const leaveModalSubmitBtn = document.getElementById('leave-modal-submit-btn');
    const clothingDescInput = document.getElementById('clothing-desc-input');
    const lastPlanDate = document.getElementById('last-plan-date');
    const planDueDate = document.getElementById('plan-due-date');
    const lastHonosDate = document.getElementById('last-honos-date');
    const honosDueDate = document.getElementById('honos-due-date');
    const lastUdsDate = document.getElementById('last-uds-date');
    const udsDueDate = document.getElementById('uds-due-date');
    const udsFrequencySelect = document.getElementById('uds-frequency-select');
    const mdtDaySelect = document.getElementById('mdt-day-select');
    const modal = document.getElementById('date-picker-modal');
    const modalTitle = document.getElementById('modal-title');
    const modalCancelBtn = document.getElementById('modal-cancel-btn');
    const modalSaveBtn = document.getElementById('modal-save-btn');
    const modalTodayBtn = document.getElementById('modal-today-btn');
    const leavesTodayList = document.getElementById('leaves-today-list');
    const allLeavesList = document.getElementById('all-leaves-list');
    const leaveModalCancelBtn = document.getElementById('leave-modal-cancel-btn');
    const leaveTypeEscortedRadio = document.getElementById('leave-type-escorted');
    const leaveTypeUnescortedRadio = document.getElementById('leave-type-unescorted');

    const taskToggles = {
        'rel_security': document.getElementById('rel-security-toggle'), 'profile': document.getElementById('profile-toggle'),
        'metobolic': document.getElementById('metobolic-toggle'), 'bloods': document.getElementById('bloods-toggle'),
        'flight_risk': document.getElementById('flight-risk-toggle'),
    };

    let allPatients = [], selectedPatient = null, selectedLeave = null, currentDateField = null;

    async function refreshAllData(selectedIdToPreserve) {
        try {
            const response = await fetch(PATIENTS_API);
            allPatients = await response.json();
            renderPatientList();
            if (selectedIdToPreserve) {
                handlePatientSelection(selectedIdToPreserve);
            }
        } catch (error) { console.error("Error refreshing data:", error); }
    }

    function renderPatientList() {
        if (!patientListContainer) return;
        const currentScroll = patientListContainer.scrollTop;
        patientListContainer.innerHTML = '';
        allPatients.forEach(person => {
            if (person.nhi) {
                const item = document.createElement('div');
                item.className = 'patient-list-item';
                item.dataset.patientId = person.id;
                item.innerHTML = `<strong>${person.name}</strong><br><small>${person.nhi} - Room: ${person.room}</small>`;
                item.addEventListener('click', () => handlePatientSelection(person.id));
                patientListContainer.appendChild(item);
            }
        });
        patientListContainer.scrollTop = currentScroll;
    }
    
    function populateDetailsPane() {
        if (!selectedPatient) return;
        const formatDate = (dateString) => {
            if (!dateString) return '--';
            const date = new Date(dateString);
            if (isNaN(date)) return '--'; 
            return date.toLocaleDateString('en-NZ');
        };
        lastPlanDate.textContent = formatDate(selectedPatient.last_treatment_plan);
        planDueDate.textContent = formatDate(selectedPatient.treatment_plans_due);
        lastHonosDate.textContent = formatDate(selectedPatient.last_honos);
        honosDueDate.textContent = formatDate(selectedPatient.honos_due);
        lastUdsDate.textContent = formatDate(selectedPatient.last_uds);
        udsDueDate.textContent = formatDate(selectedPatient.uds_due);
        udsFrequencySelect.innerHTML = UDS_OPTIONS.map(o => `<option value="${o}" ${selectedPatient.uds_frequency === o ? 'selected' : ''}>${o}</option>`).join('');
        mdtDaySelect.innerHTML = MDT_DAYS.map(d => `<option value="${d}" ${selectedPatient.mdt_day === d ? 'selected' : ''}>${d}</option>`).join('');
        for (const taskName in taskToggles) {
            const btn = taskToggles[taskName];
            if(btn) {
                const isDone = selectedPatient[taskName];
                btn.textContent = isDone ? 'Done' : 'Not Done';
                btn.className = 'task-toggle-btn';
                btn.classList.add(isDone ? 'done' : 'not-done');
            }
        }
    }

    async function populateLeaveLists() {
        if (!selectedPatient) return;
        leavesTodayList.innerHTML = '';
        allLeavesList.innerHTML = '';
        selectedLeave = null;
        try {
            const response = await fetch(`/api/people/${selectedPatient.id}/leaves`);
            if (!response.ok) throw new Error('Failed to fetch leave data');
            const leaves = await response.json();
            if (leaves.length === 0) {
                leavesTodayList.innerHTML = '<div class="leave-item">No leaves recorded.</div>';
                return;
            }
            const today = new Date().toLocaleDateString('en-NZ');
            leaves.forEach(leave => {
                const item = document.createElement('div');
                item.className = 'leave-item';
                item.addEventListener('click', () => handleLeaveSelection(leave, item));
                const leaveDate = new Date(leave.LeaveDate).toLocaleDateString('en-NZ');
                const leaveTime = leave.LeaveTime ? new Date(leave.LeaveTime).toLocaleTimeString('en-NZ', { hour: '2-digit', minute: '2-digit' }) : '';
                const returnTime = leave.ReturnTime ? new Date(leave.ReturnTime).toLocaleTimeString('en-NZ', { hour: '2-digit', minute: '2-digit' }) : 'N/A';
                item.textContent = `${leaveDate} | ${leaveTime} - ${returnTime} | ${leave.LeaveType}`;
                if (leaveDate === today) { leavesTodayList.appendChild(item); } 
                else { allLeavesList.appendChild(item); }
            });
        } catch (error) { console.error('Error populating leave lists:', error); }
    }

    async function updateField(fieldName, newValue) {
        if (!selectedPatient) return;
        try {
            const response = await fetch(`/api/people/${selectedPatient.id}/update-field`, { method: 'PATCH', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ field_name: fieldName, new_value: newValue }) });
            if (!response.ok) throw new Error('Failed to update field.');
        } catch (error) {
            console.error(`Error updating ${fieldName}:`, error);
            alert(`Could not update ${fieldName}.`);
            throw error;
        }
    }

    function handlePatientSelection(patientId) {
        selectedPatient = allPatients.find(p => p.id === patientId);
        if (!selectedPatient) {
            detailsPane.classList.add('hidden');
            return;
        }
        document.querySelectorAll('.patient-list-item').forEach(item => {
            item.classList.toggle('selected', item.dataset.patientId == patientId);
        });
        detailsPane.classList.remove('hidden');
        detailsHeader.textContent = `Currently Managing: ${selectedPatient.name}`;
        detailsPane.classList.toggle('is-special', selectedPatient.is_special_patient);
        populateDetailsPane();
        populateLeaveLists();
    }
    
    function handleLeaveSelection(leaveObject, leaveElement) {
        selectedLeave = leaveObject;
        console.log("Selected Leave:", selectedLeave);
        document.querySelectorAll('.leave-item').forEach(item => item.classList.remove('selected'));
        leaveElement.classList.add('selected');
    }

    function openDatePicker(field, title) {
        currentDateField = field;
        modalTitle.textContent = title;
        const currentDate = selectedPatient[field === 'plan' ? 'last_treatment_plan' : (field === 'honos' ? 'last_honos' : 'last_uds')];
        datePicker.setDate(currentDate ? new Date(currentDate) : new Date());
        modal.classList.remove('hidden');
    }

    function resetLeaveModalDefaults() {
        leaveTypeEscortedRadio.checked = true;
        addLeaveModal.querySelector('input[name="duration"][value="30"]').checked = true;
        clothingDescInput.value = '';
        staffResponsibleChoice.clearStore();
        staffMseChoice.clearStore();
        shiftLeadChoice.clearStore();
    }

    async function openAddLeaveModal() {
        if (!selectedPatient) {
            alert("Please select a patient first.");
            return;
        }
        
        resetLeaveModalDefaults();
        addLeaveTitle.textContent = `New Leave Checklist for ${selectedPatient.name}`;

        try {
            const [allStaff, delegatedStaff, escortedText, unescortedText] = await Promise.all([
                fetch(STAFF_API).then(res => res.json()),
                fetch(DELEGATED_STAFF_API).then(res => res.json()),
                fetch(`${UI_TEXT_API}?context=Escorted`).then(res => res.json()),
                fetch(`${UI_TEXT_API}?context=Unescorted`).then(res => res.json())
            ]);
            
            staffResponsibleChoice.setChoices(allStaff.map(s => ({ value: s.ID, label: `${s.StaffName} (${s.Role})` })), 'value', 'label', true);
            staffMseChoice.setChoices(allStaff.map(s => ({ value: s.ID, label: `${s.StaffName} (${s.Role})` })), 'value', 'label', true);
            shiftLeadChoice.setChoices(delegatedStaff.map(s => ({ value: s.ID, label: s.StaffName })), 'value', 'label', true);

            escortedChecklistContainer.innerHTML = buildChecklistHtml(escortedText, 'escorted');
            unescortedChecklistContainer.innerHTML = buildChecklistHtml(unescortedText, 'unescorted');
            
            addLeaveModal.querySelectorAll('input[name*="_phone"]').forEach(radio => {
                radio.addEventListener('change', handlePhoneSelectionChange);
            });
            addLeaveModal.querySelectorAll('input[name="duration"]').forEach(radio => {
                radio.addEventListener('change', handleDurationChange);
            });

        } catch (error) { 
            console.error("Could not load all data for leave modal:", error); 
        }
        
        handleDurationChange({ target: addLeaveModal.querySelector('input[name="duration"]:checked') });
        toggleChecklists();
        addLeaveModal.classList.remove('hidden');
    }

    function buildChecklistHtml(textData, context) {
        // --- MODIFIED: Phone options are now conditional based on the context ---
        let phoneOptions;
        if (context === 'unescorted') {
            phoneOptions = [
                { id: 'knows_contact', label: 'Knows how to contact ward' },
                { id: 'own', label: textData.optOwnPhone || 'Own Phone' }
            ];
        } else { // Escorted
            phoneOptions = [
                { id: 'ward1', label: textData.optWardOne || 'Ward Phone 1' },
                { id: 'ward2', label: textData.optWardTwo || 'Ward Phone 2' },
                { id: 'ward3', label: textData.optWardThree || 'Ward Phone 3' },
                { id: 'own', label: textData.optOwnPhone || 'Own Phone' }
            ];
        }

        const phoneRadiosHtml = phoneOptions.map((opt, index) => `
            <div><label><input type="radio" name="${context}_phone" value="${opt.id}" ${index === 0 ? 'checked' : ''}> ${opt.label}</label></div>
        `).join('');

        const leaveTypeOptions = context === 'escorted'
            ? [{ id: 'EGA', label: 'Escorted Ground Access (EGA)' }, { id: 'ECL', label: 'Escorted Community Leave (ECL)' }]
            : [{ id: 'UGA', label: 'Unescorted Ground Access (UGA)' }, { id: 'UCL', label: 'Unescorted Community Leave (UCL)' }];
        
        const leaveTypeRadiosHtml = leaveTypeOptions.map((opt, index) => `
            <label style="margin-right: 15px;"><input type="radio" name="${context}_leave_type" value="${opt.id}" ${index === 0 ? 'checked' : ''}> ${opt.label}</label>
        `).join('');

        return `
            <div class="form-group"><label>Select Leave Type:</label><div>${leaveTypeRadiosHtml}</div></div><hr>
            <div class="form-group"><label>Mental State Exam:</label><p class="checklist-desc">${textData.lblMSE || ''}</p><div><label><input type="radio" name="${context}_mse" value="rn" checked> ${textData.optMSE_RN || 'Completed by RN'}</label></div><div><label><input type="radio" name="${context}_mse" value="other"> ${textData.optMSE_Other || 'Completed by HCA'}</label></div></div>
            <div class="form-group"><label>Risk Assessment:</label><p class="checklist-desc">${textData.lblRisk || ''}</p><div><label><input type="radio" name="${context}_risk" value="rn" checked> ${textData.optRiskAssessmentRN || 'Completed by RN'}</label></div><div><label><input type="radio" name="${context}_risk" value="other"> ${textData.optRiskAssessment_Other || 'Completed by HCA'}</label></div></div>
            <div class="form-group"><label>Awareness of Leave Conditions:</label><p class="checklist-desc">${textData.lblLeaveCondition || ''}</p><div><label><input type="checkbox" name="${context}_leave_con"> ${textData.chkLeaveCon || 'I am aware'}</label></div></div>
            <div class="form-group"><label>Awareness of AWOL Procedure:</label><p class="checklist-desc">${textData.lblAWOL || ''}</p><div><label><input type="checkbox" name="${context}_awol"> ${textData.chkAwol || 'I am aware'}</label></div></div>
            <div class="form-group">
                <label>Ability to Contact Ward:</label><p class="checklist-desc">${textData.lbContactWard || ''}</p>
                ${phoneRadiosHtml}
                <div id="${context}-own-phone-container" class="hidden" style="margin-top: 10px;">
                    <label for="${context}-phone-number-input">Patient's Phone Number:</label>
                    <input type="tel" id="${context}-phone-number-input" placeholder="Enter phone number">
                </div>
            </div>
        `;
    }

    function handlePhoneSelectionChange(event) {
        const context = event.target.name.split('_')[0];
        const ownPhoneContainer = document.getElementById(`${context}-own-phone-container`);
        if (event.target.value === 'own') {
            ownPhoneContainer.classList.remove('hidden');
        } else {
            ownPhoneContainer.classList.add('hidden');
            document.getElementById(`${context}-phone-number-input`).value = '';
        }
    }
    
    function handleDurationChange(event) {
        const durationOtherInput = document.getElementById('duration-other-input');
        if (event.target.value === 'other') {
            durationOtherInput.classList.remove('hidden');
        } else {
            durationOtherInput.classList.add('hidden');
            durationOtherInput.value = '';
        }
    }
    
    function validateLeaveForm() {
        const errors = [];
        if (!staffResponsibleChoice.getValue(true)) errors.push("Staff Responsible must be selected.");
        if (!staffMseChoice.getValue(true)) errors.push("Staff Completing MSE must be selected.");
        if (!shiftLeadChoice.getValue(true)) errors.push("Shift Lead Notified must be selected.");
        if (clothingDescInput.value.trim().length === 0) errors.push("Description of Clothing cannot be empty.");

        const durationSelection = addLeaveModal.querySelector('input[name="duration"]:checked').value;
        const otherDurationValue = document.getElementById('duration-other-input').value;
        if (durationSelection === 'other' && (!otherDurationValue || parseInt(otherDurationValue, 10) <= 0)) {
            errors.push("A valid duration in minutes is required when 'Other' is selected.");
        }

        const context = addLeaveModal.querySelector('input[name="leave-type"]:checked').value.toLowerCase();
        const phoneSelection = addLeaveModal.querySelector(`input[name="${context}_phone"]:checked`).value;
        const ownPhoneNumber = document.getElementById(`${context}-phone-number-input`).value.trim();
        if (phoneSelection === 'own' && ownPhoneNumber.length === 0) {
            errors.push("Patient's phone number must be entered when 'Own Phone' is selected.");
        }

        const leaveConCheckbox = addLeaveModal.querySelector(`input[name="${context}_leave_con"]`);
        const awolCheckbox = addLeaveModal.querySelector(`input[name="${context}_awol"]`);
        if (!leaveConCheckbox || !leaveConCheckbox.checked) {
            errors.push("You must confirm awareness of Leave Conditions.");
        }
        if (!awolCheckbox || !awolCheckbox.checked) {
            errors.push("You must confirm awareness of the AWOL Procedure.");
        }

        if (errors.length > 0) {
            alert("Please complete all required fields:\n\n- " + errors.join("\n- "));
            return false;
        }
        return true;
    }
    
    function toggleChecklists() {
        const isEscorted = leaveTypeEscortedRadio.checked;
        escortedChecklistContainer.classList.toggle('hidden', !isEscorted);
        unescortedChecklistContainer.classList.toggle('hidden', isEscorted);
    }
    
    // --- EVENT LISTENERS ---
    modalCancelBtn.addEventListener('click', () => modal.classList.add('hidden'));
    modalTodayBtn.addEventListener('click', () => datePicker.setDate(new Date(), true));
    modalSaveBtn.addEventListener('click', async () => {
        const selectedDate = datePicker.selectedDates[0];
        if (!selectedDate || !currentDateField || !selectedPatient) return;
        const newDate = flatpickr.formatDate(selectedDate, "d/m/Y"); 
        let endpoint = '', body = {};
        const patientId = selectedPatient.id;
        if (currentDateField === 'plan') {
            endpoint = `/api/people/${patientId}/update-plan-date`; body = { completed_date: newDate };
        } else if (currentDateField === 'honos') {
            endpoint = `/api/people/${patientId}/update-honos-date`; body = { completed_date: newDate };
        } else if (currentDateField === 'uds') {
            endpoint = `/api/people/${patientId}/update-uds-date`; body = { last_test_date: newDate };
        }
        try {
            const response = await fetch(endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
            if (!response.ok) throw new Error('Update failed');
            modal.classList.add('hidden');
            await refreshAllData(patientId);
        } catch (error) {
            console.error('Error updating date:', error);
            alert('Could not update the date.');
        }
    });

    document.getElementById('last-plan-date').addEventListener('click', () => openDatePicker('plan', 'Change Last Plan Date'));
    document.getElementById('last-honos-date').addEventListener('click', () => openDatePicker('honos', 'Change Last HoNos Date'));
    document.getElementById('last-uds-date').addEventListener('click', () => openDatePicker('uds', 'Change Last UDS Date'));
    document.getElementById('add-leave-btn').addEventListener('click', openAddLeaveModal);

    leaveModalCancelBtn.addEventListener('click', () => addLeaveModal.classList.add('hidden'));
    leaveTypeEscortedRadio.addEventListener('change', toggleChecklists);
    leaveTypeUnescortedRadio.addEventListener('change', toggleChecklists);
    
    leaveModalSubmitBtn.addEventListener('click', async () => {
        if (!selectedPatient || !validateLeaveForm()) return;

        leaveModalSubmitBtn.disabled = true;
        leaveModalSubmitBtn.textContent = 'Submitting...';

        let duration = addLeaveModal.querySelector('input[name="duration"]:checked').value;
        if (duration === 'other') {
            duration = document.getElementById('duration-other-input').value;
        }

        const isEscorted = addLeaveModal.querySelector('input[name="leave-type"]:checked').value === 'Escorted';
        const context = isEscorted ? 'escorted' : 'unescorted';
        const phoneRadio = addLeaveModal.querySelector(`input[name="${context}_phone"]:checked`);
        const phoneSelection = phoneRadio.value;
        const ownPhoneNumber = document.getElementById(`${context}-phone-number-input`).value.trim();
        const leaveType = addLeaveModal.querySelector(`input[name="${context}_leave_type"]:checked`).value;
        
        // --- MODIFIED: Logic to get the correct contact phone number ---
        let contactPhoneNumber = null;
        if (phoneSelection === 'own') {
            contactPhoneNumber = ownPhoneNumber;
        } else if (phoneSelection === 'knows_contact') {
            contactPhoneNumber = '0';
        } else { // It's a ward phone
            const labelText = phoneRadio.closest('label').textContent;
            const match = labelText.match(/(\d{3}[\s-]?\d{3}[\s-]?\d{3,4}|\d{10,11})/);
            if (match) {
                contactPhoneNumber = match[0];
            }
        }

        const leaveData = {
            nhi: selectedPatient.nhi,
            patient_name: selectedPatient.name,
            leave_type: leaveType,
            is_escorted_leave: isEscorted,
            duration_minutes: duration,
            staff_responsible_id: staffResponsibleChoice.getValue(true),
            staff_mse_id: staffMseChoice.getValue(true),
            senior_nurse_id: shiftLeadChoice.getValue(true),
            leave_description: clothingDescInput.value.trim(),
            contact_phone_number: contactPhoneNumber,
            mse_completed: addLeaveModal.querySelector(`input[name="${context}_mse"]:checked`)?.value === 'rn',
            risk_assessment_completed: addLeaveModal.querySelector(`input[name="${context}_risk"]:checked`)?.value === 'rn',
            leave_conditions_met: addLeaveModal.querySelector(`input[name="${context}_leave_con"]`)?.checked || false,
            awol_aware: addLeaveModal.querySelector(`input[name="${context}_awol"]`)?.checked || false,
            contact_aware: true,
        };

        try {
            const response = await fetch(LEAVES_API, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(leaveData)
            });
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Failed to save leave record.');
            }
            alert('Leave saved successfully!');
            addLeaveModal.classList.add('hidden');
            await refreshAllData(selectedPatient.id);
        } catch (error) {
            console.error('Error saving leave:', error);
            alert(`Could not save leave: ${error.message}`);
        } finally {
            leaveModalSubmitBtn.disabled = false;
            leaveModalSubmitBtn.textContent = 'Submit';
        }
    });

    for (const taskName in taskToggles) {
        taskToggles[taskName].addEventListener('click', async () => {
            if (!selectedPatient) return;
            const patientId = selectedPatient.id;
            await updateField(taskName, !selectedPatient[taskName]);
            await refreshAllData(patientId);
        });
    }

    udsFrequencySelect.addEventListener('change', async (event) => {
        if (!selectedPatient) return;
        const patientId = selectedPatient.id;
        await updateField('uds_frequency', event.target.value);
        const lastUds = selectedPatient.last_uds ? new Date(selectedPatient.last_uds).toLocaleDateString('en-NZ') : new Date().toLocaleDateString('en-NZ');
        try {
            await fetch(`/api/people/${patientId}/update-uds-date`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ last_test_date: lastUds }) });
            await refreshAllData(patientId);
        } catch (error) { console.error('Error recalculating UDS date:', error); }
    });

    mdtDaySelect.addEventListener('change', async (event) => {
        if (!selectedPatient) return;
        const patientId = selectedPatient.id;
        await updateField('mdt_day', event.target.value);
        await refreshAllData(patientId);
    });

    // --- INITIALIZE ---
    refreshAllData();
});