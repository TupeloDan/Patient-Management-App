document.addEventListener('DOMContentLoaded', () => {
    // --- Initialize the date picker ---
    const datePicker = flatpickr("#modal-date-input", {
        dateFormat: "d/m/Y", // Sets the DD/MM/YYYY format
    });

    // --- API Endpoints & Config ---
    const PATIENTS_API = '/api/people';
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

    const taskToggles = {
        'rel_security': document.getElementById('rel-security-toggle'), 'profile': document.getElementById('profile-toggle'),
        'metobolic': document.getElementById('metobolic-toggle'), 'bloods': document.getElementById('bloods-toggle'),
        'flight_risk': document.getElementById('flight-risk-toggle'),
    };

    let allPatients = [], selectedPatient = null, currentDateField = null;

    /**
     * Fetches all data, re-renders the patient list, and re-selects the current patient.
     */
    async function refreshAllData(selectedIdToPreserve) {
        try {
            const response = await fetch(PATIENTS_API);
            allPatients = await response.json();
            renderPatientList();
            if (selectedIdToPreserve) {
                handlePatientSelection(selectedIdToPreserve, false); // false to prevent loop
            }
        } catch (error) {
            console.error("Error refreshing data:", error);
        }
    }

    /**
     * Renders the clickable patient list on the left.
     */
    function renderPatientList() {
        const currentScroll = patientListContainer.scrollTop;
        patientListContainer.innerHTML = '';
        allPatients.forEach(person => {
            if (person.nhi) {
                const item = document.createElement('div');
                item.className = 'patient-list-item';
                item.dataset.patientId = person.id;
                item.innerHTML = `<strong>${person.name}</strong><br><small>${person.nhi} - Room: ${person.room}</small>`;
                item.addEventListener('click', () => handlePatientSelection(person.id, true)); // true to fetch leaves
                patientListContainer.appendChild(item);
            }
        });
        patientListContainer.scrollTop = currentScroll;
    }
    
    /**
     * Populates the details pane with the selected patient's task data.
     */
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
            const btn = taskToggles[taskName], isDone = selectedPatient[taskName];
            btn.textContent = isDone ? 'Done' : 'Not Done';
            btn.className = 'task-toggle-btn';
            btn.classList.add(isDone ? 'done' : 'not-done');
        }
    }

    /**
     * Fetches and displays leave records for the selected patient.
     */
    async function populateLeaveLists() {
        if (!selectedPatient) return;
        leavesTodayList.innerHTML = '';
        allLeavesList.innerHTML = '';
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
                const leaveDate = new Date(leave.LeaveDate).toLocaleDateString('en-NZ');
                const leaveTime = leave.LeaveTime ? new Date(leave.LeaveTime).toLocaleTimeString('en-NZ', { hour: '2-digit', minute: '2-digit' }) : '';
                const returnTime = leave.ReturnTime ? new Date(leave.ReturnTime).toLocaleTimeString('en-NZ', { hour: '2-digit', minute: '2-digit' }) : 'N/A';
                item.textContent = `${leaveDate} | ${leaveTime} - ${returnTime} | ${leave.LeaveType}`;
                if (leaveDate === today) { leavesTodayList.appendChild(item); } 
                else { allLeavesList.appendChild(item); }
            });
        } catch (error) { console.error('Error populating leave lists:', error); }
    }

    /**
     * Sends a request to update a single field in the database.
     */
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

    /**
     * Handles the logic for when a patient is selected from the list.
     */
    function handlePatientSelection(patientId, shouldFetchLeaves = true) {
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
        if (shouldFetchLeaves) {
            populateLeaveLists();
        }
    }

    // --- MODAL & EVENT LISTENERS ---
    function openDatePicker(field, title) {
        currentDateField = field;
        modalTitle.textContent = title;
        const currentDate = selectedPatient[field === 'plan' ? 'last_treatment_plan' : (field === 'honos' ? 'last_honos' : 'last_uds')];
        datePicker.setDate(currentDate ? new Date(currentDate) : new Date());
        modal.classList.remove('hidden');
    }

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
            alert('Could not update the date. Please check the terminal for more details.');
        }
    });

    lastPlanDate.addEventListener('click', () => openDatePicker('plan', 'Change Last Plan Date'));
    lastHonosDate.addEventListener('click', () => openDatePicker('honos', 'Change Last HoNos Date'));
    lastUdsDate.addEventListener('click', () => openDatePicker('uds', 'Change Last UDS Date'));

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