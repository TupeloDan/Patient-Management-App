document.addEventListener('DOMContentLoaded', () => {
    // --- Initializations ---
    const datePicker = flatpickr("#modal-date-input", { dateFormat: "d/m/Y" });
    const staffResponsibleChoice = new Choices('#staff-responsible-select', { removeItemButton: true, searchResultLimit: 10 });
    const staffMseChoice = new Choices('#staff-mse-select', { removeItemButton: true, searchResultLimit: 10 });
    const shiftLeadChoice = new Choices('#shift-lead-select', { removeItemButton: true, searchResultLimit: 10 });

    // --- API Endpoints & Config ---
    const PATIENTS_API = '/api/people';
    const STAFF_API = '/api/staff';
    const DELEGATED_STAFF_API = '/api/delegated-staff'; // NEW
    const UI_TEXT_API = '/api/ui-text';
    const LEAVES_API = '/api/leaves';
    const UDS_OPTIONS = ['Weekly', 'Bi-Weekly', 'Monthly', 'Random', 'OnRequest'];
    const MDT_DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];

    // --- DOM Elements ---
    const patientListContainer = document.getElementById('patient-list-container');
    const detailsPane = document.getElementById('details-pane');
    const detailsHeader = document.getElementById('details-header');
    const specialPatientLabel = document.getElementById('special-patient-label');
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
    const modalDateInput = document.getElementById('modal-date-input');
    const modalCancelBtn = document.getElementById('modal-cancel-btn');
    const modalSaveBtn = document.getElementById('modal-save-btn');
    const modalTodayBtn = document.getElementById('modal-today-btn');
    const leavesTodayList = document.getElementById('leaves-today-list');
    const allLeavesList = document.getElementById('all-leaves-list');
    const addLeaveBtn = document.getElementById('add-leave-btn');
    const addLeaveModal = document.getElementById('add-leave-modal');
    const addLeaveTitle = document.getElementById('add-leave-title');
    const leaveModalCancelBtn = document.getElementById('leave-modal-cancel-btn');
    const leaveModalSubmitBtn = document.getElementById('leave-modal-submit-btn');
    const leaveTypeEscortedRadio = document.getElementById('leave-type-escorted');
    const leaveTypeUnescortedRadio = document.getElementById('leave-type-unescorted');
    const escortedChecklistContainer = document.getElementById('escorted-checklist-container');
    const unescortedChecklistContainer = document.getElementById('unescorted-checklist-container');
    const clothingDescInput = document.getElementById('clothing-desc-input');

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

    async function openAddLeaveModal() {
        if (!selectedPatient) {
            alert("Please select a patient first.");
            return;
        }
        addLeaveTitle.textContent = `New Leave Checklist for ${selectedPatient.name}`;
        try {
            // --- REFINED: Fetch all three staff lists in parallel ---
            const [allStaff, delegatedStaff] = await Promise.all([
                fetch(STAFF_API).then(res => res.json()),
                fetch(DELEGATED_STAFF_API).then(res => res.json())
            ]);
            
            const staffChoices = allStaff.map(s => ({ value: s.ID, label: `${s.StaffName} (${s.Role})` }));
            const delegatedChoices = delegatedStaff.map(s => ({ value: s.ID, label: s.StaffName }));

            staffResponsibleChoice.setChoices(staffChoices, 'value', 'label', true);
            staffMseChoice.setChoices(staffChoices, 'value', 'label', true);
            shiftLeadChoice.setChoices(delegatedChoices, 'value', 'label', true);

        } catch (error) { console.error("Could not load staff for leave modal:", error); }
        
        try {
            const escortedTextResponse = await fetch(`${UI_TEXT_API}?context=Escorted`);
            const escortedText = await escortedTextResponse.json();
            const unescortedTextResponse = await fetch(`${UI_TEXT_API}?context=Unescorted`);
            const unescortedText = await unescortedTextResponse.json();
            escortedChecklistContainer.innerHTML = buildChecklistHtml(escortedText, 'escorted');
            unescortedChecklistContainer.innerHTML = buildChecklistHtml(unescortedText, 'unescorted');
        } catch (error) { console.error("Could not load UI text for checklists:", error); }
        toggleChecklists();
        addLeaveModal.classList.remove('hidden');
    }

    function buildChecklistHtml(textData, context) {
        return `
            <div class="form-group"><label>Mental State Exam:</label><p class="checklist-desc">${textData.lblMSE || ''}</p><div><label><input type="radio" name="${context}_mse" value="rn" checked> ${textData.optMSE_RN || 'Completed by RN'}</label></div><div><label><input type="radio" name="${context}_mse" value="other"> ${textData.optMSE_Other || 'Completed by HCA'}</label></div></div>
            <div class="form-group"><label>Risk Assessment:</label><p class="checklist-desc">${textData.lblRisk || ''}</p><div><label><input type="radio" name="${context}_risk" value="rn" checked> ${textData.optRiskAssessmentRN || 'Completed by RN'}</label></div><div><label><input type="radio" name="${context}_risk" value="other"> ${textData.optRiskAssessment_Other || 'Completed by HCA'}</label></div></div>
            <div class="form-group"><label>Awareness of Leave Conditions:</label><p class="checklist-desc">${textData.lblLeaveCondition || ''}</p><div><label><input type="checkbox" name="${context}_leave_con"> ${textData.chkLeaveCon || 'I am aware'}</label></div></div>
            <div class="form-group"><label>Awareness of AWOL Procedure:</label><p class="checklist-desc">${textData.lblAWOL || ''}</p><div><label><input type="checkbox" name="${context}_awol"> ${textData.chkAwol || 'I am aware'}</label></div></div>
            <div class="form-group"><label>Ability to Contact Ward:</label><p class="checklist-desc">${textData.lbContactWard || ''}</p><div><label><input type="radio" name="${context}_phone" value="ward1" checked> ${textData.optWardOne || 'Ward Phone 1'}</label></div><div><label><input type="radio" name="${context}_phone" value="ward2"> ${textData.optWardTwo || 'Ward Phone 2'}</label></div><div><label><input type="radio" name="${context}_phone" value="own"> ${textData.optOwnPhone || 'Own Phone'}</label></div></div>
        `;
    }

    function toggleChecklists() {
        if (leaveTypeEscortedRadio.checked) {
            escortedChecklistContainer.classList.remove('hidden');
            unescortedChecklistContainer.classList.add('hidden');
        } else {
            escortedChecklistContainer.classList.add('hidden');
            unescortedChecklistContainer.classList.remove('hidden');
        }
    }
    
    // --- REFINED: Added a validation function for clarity ---
    function validateLeaveForm() {
        const staffResp = staffResponsibleChoice.getValue(true);
        const shiftLead = shiftLeadChoice.getValue(true);
        const clothingDesc = clothingDescInput.value.trim();
        
        const errors = [];
        if (!staffResp) {
            errors.push("Staff Responsible must be selected.");
        }
        if (!shiftLead) {
            errors.push("Shift Lead Notified must be selected.");
        }
        if (clothingDesc.length === 0) {
            errors.push("Description of Clothing cannot be empty.");
        }

        if (errors.length > 0) {
            alert("Please fix the following issues:\n\n- " + errors.join("\n- "));
            return false;
        }
        return true;
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

    lastPlanDate.addEventListener('click', () => openDatePicker('plan', 'Change Last Plan Date'));
    lastHonosDate.addEventListener('click', () => openDatePicker('honos', 'Change Last HoNos Date'));
    lastUdsDate.addEventListener('click', () => openDatePicker('uds', 'Change Last UDS Date'));

    addLeaveBtn.addEventListener('click', openAddLeaveModal);
    leaveModalCancelBtn.addEventListener('click', () => addLeaveModal.classList.add('hidden'));
    leaveTypeEscortedRadio.addEventListener('change', toggleChecklists);
    leaveTypeUnescortedRadio.addEventListener('change', toggleChecklists);
    
    // --- REFINED: The entire submit button logic is updated ---
    leaveModalSubmitBtn.addEventListener('click', async () => {
        if (!selectedPatient || !validateLeaveForm()) {
            return;
        }

        // --- REFINED: Disable button to prevent double-clicks ---
        leaveModalSubmitBtn.disabled = true;
        leaveModalSubmitBtn.textContent = 'Submitting...';

        const leaveType = document.querySelector('input[name="leave-type"]:checked').value;
        const context = leaveType.toLowerCase();
        const duration = document.querySelector('input[name="duration"]:checked').value;
        const checklistContainer = document.getElementById(`${context}-checklist-container`);
        
        const leaveData = {
            nhi: selectedPatient.nhi,
            patient_name: selectedPatient.name,
            leave_type: leaveType,
            is_escorted_leave: leaveType === 'Escorted',
            duration_minutes: duration,
            staff_responsible_id: staffResponsibleChoice.getValue(true),
            senior_nurse_id: shiftLeadChoice.getValue(true), // MODIFIED
            leave_description: clothingDescInput.value.trim(),
            // --- The rest of the checklist data ---
            mse_completed: checklistContainer.querySelector(`input[name="${context}_mse"]:checked`)?.value === 'rn',
            risk_assessment_completed: checklistContainer.querySelector(`input[name="${context}_risk"]:checked`)?.value === 'rn',
            leave_conditions_met: checklistContainer.querySelector(`input[name="${context}_leave_con"]`)?.checked || false,
            awol_aware: checklistContainer.querySelector(`input[name="${context}_awol"]`)?.checked || false,
            contact_aware: checklistContainer.querySelector(`input[name="${context}_phone"]:checked`)?.value !== 'ward1' && checklistContainer.querySelector(`input[name="${context}_phone"]:checked`)?.value !== 'ward2',
        };

        try {
            const response = await fetch(LEAVES_API, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(leaveData)
            });
            if (!response.ok) {
                // Try to get a specific error message from the backend
                const errorData = await response.json();
                throw new Error(errorData.error || 'Failed to save leave record.');
            }
            alert('Leave saved successfully!');
            addLeaveModal.classList.add('hidden');
            await refreshAllData(selectedPatient.id);
        } catch (error) {
            console.error('Error saving leave:', error);
            // --- REFINED: Show the specific error from the backend ---
            alert(`Could not save leave: ${error.message}`);
        } finally {
            // --- REFINED: Re-enable the button regardless of success or failure ---
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