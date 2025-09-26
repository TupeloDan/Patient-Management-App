document.addEventListener('DOMContentLoaded', () => {
    // --- API Endpoints ---
    const PATIENTS_API = '/api/people';
    const STAFF_API = '/api/staff';

    // --- DOM Elements ---
    const patientSelect = document.getElementById('patient-select');
    const assignmentForm = document.getElementById('assignment-form');
    const clinicianSelect = document.getElementById('clinician-select');
    const availableStaffList = document.getElementById('available-staff-list');
    const casemanagerList = document.getElementById('casemanager-list');
    const associateList = document.getElementById('associate-list');
    const assignCmBtn = document.getElementById('assign-cm');
    const removeCmBtn = document.getElementById('remove-cm');
    const assignAssocBtn = document.getElementById('assign-assoc');
    const removeAssocBtn = document.getElementById('remove-assoc');
    const saveBtn = document.getElementById('save-assignments');
    const cancelBtn = document.getElementById('cancel-assignments');

    // --- State Variables ---
    let allPatients = [];
    let allStaff = [];
    let selectedPatient = null;

    // --- DATA LOADING FUNCTIONS ---

    /**
     * Fetches the complete list of patients and populates the main dropdown.
     */
    async function loadPatients() {
        try {
            const response = await fetch(PATIENTS_API);
            allPatients = await response.json();
            patientSelect.innerHTML = '<option value="">Select a patient...</option>';
            allPatients.forEach(person => {
                if (person.nhi) { // Only list patients who have an NHI
                    const option = document.createElement('option');
                    option.value = person.id;
                    option.textContent = `${person.name} (${person.nhi})`;
                    patientSelect.appendChild(option);
                }
            });
        } catch (error) {
            console.error('Error loading patients:', error);
        }
    }

    /**
     * Fetches the complete, unfiltered list of staff.
     */
    async function loadStaff() {
        try {
            // Fetches ALL staff to allow for client-side filtering into different roles
            const response = await fetch(STAFF_API);
            allStaff = await response.json();
        } catch (error) {
            console.error('Error loading staff:', error);
        }
    }

    // --- UI LOGIC FUNCTIONS ---

    /**
     * Clears all staff lists and hides the main assignment form.
     */
    function clearAssignmentForm() {
        clinicianSelect.innerHTML = '';
        availableStaffList.innerHTML = '';
        casemanagerList.innerHTML = '';
        associateList.innerHTML = '';
        assignmentForm.classList.add('hidden');
    }

    /**
     * Populates all staff lists based on the selected patient's current assignments.
     * @param {object} patient - The full data object for the selected patient.
     */
    /**
     * Populates all staff lists based on the selected patient's current assignments.
     * @param {object} patient - The full data object for the selected patient.
     */
    function populateStaffLists(patient) {
        clearAssignmentForm();
        if (!patient) return;

        // --- NEW: Define the roles you want to see in the "Available" list ---
        const availableRoles = ['RN', 'EN'];

        allStaff.forEach(staff => {
            const option = document.createElement('option');
            option.value = staff.ID;
            option.textContent = `${staff.StaffName} (${staff.Role})`;

            // Populate the clinician dropdown with anyone whose role is 'RC'
            if (staff.Role === 'RC' || staff.Role === 'Responsible Clinician') {
                clinicianSelect.appendChild(option.cloneNode(true));
            }

            // Check existing assignments to sort staff into the correct lists
            const isCaseManager = (staff.ID === patient.case_manager_id || staff.ID === patient.case_manager_2nd_id);
            const isAssociate = (staff.ID === patient.associate_id || staff.ID === patient.associate_2nd_id);
            const isClinician = (staff.ID === patient.clinician_id);

            if (isCaseManager) {
                casemanagerList.appendChild(option);
            } else if (isAssociate) {
                associateList.appendChild(option);
            } else if (!isClinician && availableRoles.includes(staff.Role)) {
                // MODIFIED: Only add staff to "Available" if their role is in our list
                availableStaffList.appendChild(option);
            }
        });

        // Set the currently assigned clinician in the dropdown
        clinicianSelect.value = patient.clinician_id;
        assignmentForm.classList.remove('hidden'); // Show the populated form
    }

    /**
     * Moves selected options between two lists, enforcing an assignment limit.
     * @param {HTMLSelectElement} sourceSelect - The list to move from.
     * @param {HTMLSelectElement} destSelect - The list to move to.
     * @param {number|null} limit - The maximum number of items allowed in the destination list.
     */
    function moveSelectedOptions(sourceSelect, destSelect, limit) {
        const selectedOptions = Array.from(sourceSelect.selectedOptions);

        if (limit && (destSelect.options.length + selectedOptions.length > limit)) {
            alert(`You can only assign a maximum of ${limit} people to this role.`);
            return;
        }

        selectedOptions.forEach(option => destSelect.appendChild(option));
    }


    // --- EVENT LISTENERS ---

    patientSelect.addEventListener('change', () => {
        const selectedPatientId = patientSelect.value;
        if (selectedPatientId) {
            selectedPatient = allPatients.find(p => p.id === Number(selectedPatientId));
            if (selectedPatient) {
                console.log("Selected Patient:", selectedPatient);
                populateStaffLists(selectedPatient);
            } else {
                clearAssignmentForm();
            }
        } else {
            selectedPatient = null;
            clearAssignmentForm();
        }
    });

    // Button event listeners with assignment limits
    assignCmBtn.addEventListener('click', () => moveSelectedOptions(availableStaffList, casemanagerList, 2));
    removeCmBtn.addEventListener('click', () => moveSelectedOptions(casemanagerList, availableStaffList, null));
    assignAssocBtn.addEventListener('click', () => moveSelectedOptions(availableStaffList, associateList, 2));
    removeAssocBtn.addEventListener('click', () => moveSelectedOptions(associateList, availableStaffList, null));

    cancelBtn.addEventListener('click', () => {
        // A better cancel clears everything and resets the form to its initial state.
        patientSelect.value = ''; // Reset the main dropdown
        selectedPatient = null;
        clearAssignmentForm(); // This function clears all the lists and hides the form
    });

    saveBtn.addEventListener('click', async () => {
        if (!selectedPatient) return;

        const cmIds = Array.from(casemanagerList.options).map(opt => Number(opt.value));
        const assocIds = Array.from(associateList.options).map(opt => Number(opt.value));

        const assignmentData = {
            clinician_id: Number(clinicianSelect.value) || null,
            case_manager_id: cmIds[0] || null,
            case_manager_2nd_id: cmIds[1] || null,
            associate_id: assocIds[0] || null,
            associate_2nd_id: assocIds[1] || null
        };

        try {
            const response = await fetch(`/api/people/${selectedPatient.id}/assignments`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(assignmentData)
            });

            if (response.ok) {
                alert('Assignments saved successfully!');
                patientSelect.value = ''; // Reset dropdown
                clearAssignmentForm(); // Clear the form
                await loadPatients(); // Refresh patient data in case names/details changed
            } else {
                const errorData = await response.json();
                alert(`Failed to save assignments: ${errorData.error}`);
            }
        } catch (error) {
            console.error('Error saving assignments:', error);
            alert('An error occurred while saving.');
        }
    });

    /**
     * Initializes the editor by loading all necessary data from the server.
     */
    async function initializeEditor() {
        await loadStaff();
        await loadPatients();
    }

    // --- INITIALIZE THE EDITOR ---
    initializeEditor();
});