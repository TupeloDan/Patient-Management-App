document.addEventListener('DOMContentLoaded', () => {
    // --- API Endpoints ---
    const PATIENTS_API = '/api/people';

    // --- DOM Elements ---
    const patientListContainer = document.getElementById('patient-list-container');
    const detailsPane = document.getElementById('details-pane');
    const detailsHeader = document.getElementById('details-header');
    const specialPatientLabel = document.getElementById('special-patient-label');

    // Task Due Elements
    const lastPlanDate = document.getElementById('last-plan-date');
    const planDueDate = document.getElementById('plan-due-date');
    const lastHonosDate = document.getElementById('last-honos-date');
    const honosDueDate = document.getElementById('honos-due-date');
    const lastUdsDate = document.getElementById('last-uds-date');
    const udsDueDate = document.getElementById('uds-due-date');
    const udsFrequencySelect = document.getElementById('uds-frequency-select');
    const mdtDaySelect = document.getElementById('mdt-day-select');

    // Task Toggle Buttons
    const taskToggles = {
        'rel_security': document.getElementById('rel-security-toggle'),
        'profile': document.getElementById('profile-toggle'),
        'metobolic': document.getElementById('metobolic-toggle'),
        'bloods': document.getElementById('bloods-toggle'),
        'flight_risk': document.getElementById('flight-risk-toggle'),
    };

    let allPatients = [];
    let selectedPatient = null;

    // --- DATA LOADING ---
    async function initializePatientList() {
        try {
            const response = await fetch(PATIENTS_API);
            allPatients = await response.json();
            renderPatientList();
        } catch (error) {
            console.error("Error loading patient list:", error);
        }
    }

    // --- UI RENDERING & INTERACTION ---

    /**
     * Renders the clickable patient list on the left.
     */
    function renderPatientList() {
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
    }

    /**
     * Populates the entire details pane with the selected patient's data.
     */
    function populateDetailsPane() {
        if (!selectedPatient) return;

        const formatDate = (dateString) => dateString ? new Date(dateString).toLocaleDateString() : '--';
        lastPlanDate.textContent = formatDate(selectedPatient.last_treatment_plan);
        planDueDate.textContent = formatDate(selectedPatient.treatment_plans_due);
        lastHonosDate.textContent = formatDate(selectedPatient.last_honos);
        honosDueDate.textContent = formatDate(selectedPatient.honos_due);
        lastUdsDate.textContent = formatDate(selectedPatient.last_uds);
        udsDueDate.textContent = formatDate(selectedPatient.uds_due);

        const udsOptions = ['Weekly', 'Bi-Weekly', 'Monthly', 'Random', 'OnRequest'];
        udsFrequencySelect.innerHTML = udsOptions.map(opt => `<option value="${opt}" ${selectedPatient.uds_frequency === opt ? 'selected' : ''}>${opt}</option>`).join('');
        
        const mdtDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];
        mdtDaySelect.innerHTML = mdtDays.map(day => `<option value="${day}" ${selectedPatient.mdt_day === day ? 'selected' : ''}>${day}</option>`).join('');

        for (const taskName in taskToggles) {
            const button = taskToggles[taskName];
            const isDone = selectedPatient[taskName];
            button.textContent = isDone ? 'Done' : 'Not Done';
            button.className = 'task-toggle-btn';
            button.classList.add(isDone ? 'done' : 'not-done');
        }
    }

    /**
     * A helper function to send updates for a single field to the backend.
     */
    async function updateField(fieldName, newValue) {
        if (!selectedPatient) return;
        try {
            const response = await fetch(`/api/people/${selectedPatient.id}/update-field`, {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ field_name: fieldName, new_value: newValue })
            });
            if (!response.ok) throw new Error('Failed to update field.');
            
            // Refresh the master list of patients in the background to keep data fresh
            const freshData = await (await fetch(PATIENTS_API)).json();
            allPatients = freshData;
            // Update our selectedPatient object with the fresh data
            selectedPatient = allPatients.find(p => p.id === selectedPatient.id);

        } catch (error) {
            console.error(`Error updating ${fieldName}:`, error);
            alert(`Could not update ${fieldName}. The page will be reloaded to ensure data consistency.`);
            location.reload();
        }
    }

    /**
     * Handles what happens when a patient is clicked in the list.
     */
    function handlePatientSelection(patientId) {
        selectedPatient = allPatients.find(p => p.id === patientId);
        if (!selectedPatient) return;

        document.querySelectorAll('.patient-list-item').forEach(item => {
            item.classList.toggle('selected', item.dataset.patientId == patientId);
        });

        detailsPane.classList.remove('hidden');
        detailsHeader.textContent = `Currently Managing: ${selectedPatient.name}`;
        detailsPane.classList.toggle('is-special', selectedPatient.is_special_patient);

        populateDetailsPane();
    }

    // --- ADD EVENT LISTENERS FOR INTERACTIVE CONTROLS ---

    for (const taskName in taskToggles) {
        taskToggles[taskName].addEventListener('click', async () => {
            if (!selectedPatient) return;
            const currentValue = selectedPatient[taskName];
            const newValue = !currentValue;
            
            await updateField(taskName, newValue);
            
            // After successful save, update the UI
            populateDetailsPane();
        });
    }
    
    udsFrequencySelect.addEventListener('change', (event) => {
        updateField('uds_frequency', event.target.value);
    });

    mdtDaySelect.addEventListener('change', (event) => {
        updateField('mdt_day', event.target.value);
    });

    // --- INITIALIZE THE EDITOR ---
    initializePatientList();
});