document.addEventListener('DOMContentLoaded', () => {
    // --- DOM Elements ---
    const managementHeader = document.getElementById('management-header');
    const assignForm = document.getElementById('assign-form');
    const manageForms = document.getElementById('manage-forms');

    // Assign form elements
    const assignRoomSelect = document.getElementById('assign-room-select');
    const assignNhiInput = document.getElementById('assign-nhi');
    const assignNameInput = document.getElementById('assign-name');
    const assignLegalStatusSelect = document.getElementById('assign-legal-status');
    const assignSpecialPatientCheckbox = document.getElementById('assign-special-patient');
    const assignVnrCheckbox = document.getElementById('assign-vnr');
    const assignSpecialNotesTextarea = document.getElementById('assign-special-notes');
    const assignSubmitBtn = document.getElementById('assign-submit-btn');

    // Edit form elements
    const editNhiInput = document.getElementById('edit-nhi');
    const editNameInput = document.getElementById('edit-name');
    const editLegalStatusSelect = document.getElementById('edit-legal-status');
    const editSpecialPatientCheckbox = document.getElementById('edit-special-patient');
    const editVnrCheckbox = document.getElementById('edit-vnr');
    const editSpecialNotesTextarea = document.getElementById('edit-special-notes');
    const editSubmitBtn = document.getElementById('edit-submit-btn');

    // Assignment form elements
    const clinicianSelect = document.getElementById('clinician-select');
    const availableStaffList = document.getElementById('available-staff-list');
    const casemanagerList = document.getElementById('casemanager-list');
    const associateList = document.getElementById('associate-list');
    const assignCmBtn = document.getElementById('assign-cm');
    const removeCmBtn = document.getElementById('remove-cm');
    const assignAssocBtn = document.getElementById('assign-assoc');
    const removeAssocBtn = document.getElementById('remove-assoc');
    const saveAssignmentsBtn = document.getElementById('save-assignments-btn');
    
    // Move form elements
    const moveRoomSelect = document.getElementById('move-room-select');
    const moveSubmitBtn = document.getElementById('move-submit-btn');

    // Remove button
    const removePersonBtn = document.getElementById('remove-person-btn');

    // --- State Variables ---
    let allPeople = [];
    let allStaff = [];
    let mhaSections = [];
    let currentPerson = null;
    let personId = null;

    // --- Initialization ---
    async function initialize() {
        const params = new URLSearchParams(window.location.search);
        const action = params.get('action');
        personId = params.get('id');

        await Promise.all([
            fetch('/api/people').then(res => res.json()).then(data => allPeople = data),
            fetch('/api/mha-sections').then(res => res.json()).then(data => mhaSections = data),
            fetch('/api/staff').then(res => res.json()).then(data => allStaff = data)
        ]);
        
        if (action === 'assign') {
            setupAssignForm();
        } else if (action === 'manage' && personId) {
            currentPerson = allPeople.find(p => p.id == personId);
            if (currentPerson) {
                setupManageForms();
            } else {
                managementHeader.textContent = "Error: Person not found";
            }
        }
    }

    // --- Form Setup ---
    function setupAssignForm() {
        managementHeader.textContent = "Assign New Person";
        assignForm.classList.remove('hidden');

        allPeople.forEach(person => {
            if (!person.nhi) {
                const option = document.createElement('option');
                option.value = person.room;
                option.textContent = person.room;
                assignRoomSelect.appendChild(option);
            }
        });

        mhaSections.forEach(section => {
            const option = document.createElement('option');
            option.value = section.ID;
            option.textContent = section.LegalStatus;
            assignLegalStatusSelect.appendChild(option);
        });
    }

    function setupManageForms() {
        managementHeader.textContent = `Managing: ${currentPerson.name} (${currentPerson.room})`;
        manageForms.classList.remove('hidden');

        // Populate Edit Details Form
        editNhiInput.value = currentPerson.nhi || '';
        editNameInput.value = currentPerson.name || '';
        mhaSections.forEach(section => {
            const option = document.createElement('option');
            option.value = section.ID;
            option.textContent = section.LegalStatus;
            editLegalStatusSelect.appendChild(option);
        });
        editLegalStatusSelect.value = currentPerson.legal_id || '';
        editSpecialPatientCheckbox.checked = currentPerson.is_special_patient;
        editVnrCheckbox.checked = currentPerson.has_vnr;
        editSpecialNotesTextarea.value = currentPerson.special_notes || '';

        // Populate Staff Assignments Form
        populateStaffLists();

        // Populate Move Form
        allPeople.forEach(person => {
            if (!person.nhi) {
                const option = document.createElement('option');
                option.value = person.room;
                option.textContent = person.room;
                moveRoomSelect.appendChild(option);
            }
        });
    }

    function populateStaffLists() {
        clinicianSelect.innerHTML = '';
        availableStaffList.innerHTML = '';
        casemanagerList.innerHTML = '';
        associateList.innerHTML = '';

        const availableRoles = ['RN', 'EN'];

        allStaff.forEach(staff => {
            const option = document.createElement('option');
            option.value = staff.ID;
            option.textContent = `${staff.StaffName} (${staff.Role})`;

            if (staff.Role === 'RC' || staff.Role === 'Responsible Clinician') {
                clinicianSelect.appendChild(option.cloneNode(true));
            }

            const isCaseManager = (staff.ID === currentPerson.case_manager_id || staff.ID === currentPerson.case_manager_2nd_id);
            const isAssociate = (staff.ID === currentPerson.associate_id || staff.ID === currentPerson.associate_2nd_id);
            const isClinician = (staff.ID === currentPerson.clinician_id);

            if (isCaseManager) {
                casemanagerList.appendChild(option);
            } else if (isAssociate) {
                associateList.appendChild(option);
            } else if (!isClinician && availableRoles.includes(staff.Role)) {
                availableStaffList.appendChild(option);
            }
        });

        clinicianSelect.value = currentPerson.clinician_id || '';
    }

    function moveSelectedOptions(source, dest, limit) {
        const options = Array.from(source.selectedOptions);
        if (limit && (dest.options.length + options.length > limit)) {
            alert(`You can only assign a maximum of ${limit} people to this role.`);
            return;
        }
        options.forEach(option => dest.appendChild(option));
    }

    // --- Validation ---
    async function validateNhi(nhi, currentId = null) {
        const nhiRegex = /^[A-Z]{3}[0-9]{4}$/;
        if (!nhiRegex.test(nhi)) {
            alert('Invalid NHI format. It must be 3 uppercase letters followed by 4 numbers (e.g., ABC1234).');
            return false;
        }
        const response = await fetch(`/api/nhi/check/${nhi}`);
        const data = await response.json();
        if (data.exists) {
            const existingPerson = allPeople.find(p => p.nhi === nhi);
            if (!currentId || existingPerson.id != currentId) {
                alert('This NHI is already in use by another person.');
                return false;
            }
        }
        return true;
    }

    // --- Event Listeners ---
    assignSubmitBtn.addEventListener('click', async () => {
        const nhi = assignNhiInput.value.trim().toUpperCase();
        if (!await validateNhi(nhi)) return;

        const personData = {
            room: assignRoomSelect.value,
            nhi: nhi,
            name: assignNameInput.value.trim(),
            legal_id: assignLegalStatusSelect.value,
            is_special_patient: assignSpecialPatientCheckbox.checked,
            has_vnr: assignVnrCheckbox.checked,
            special_notes: assignSpecialNotesTextarea.value.trim()
        };

        try {
            const response = await fetch('/api/people/assign', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(personData)
            });
            if (response.ok) {
                alert('Person assigned successfully');
                window.location.href = '/main-editor';
            } else {
                alert('Error assigning person');
            }
        } catch (error) {
            console.error('Error assigning person:', error);
        }
    });

    editSubmitBtn.addEventListener('click', async () => {
        const nhi = editNhiInput.value.trim().toUpperCase();
        if (!await validateNhi(nhi, personId)) return;
        
        const personData = {
            id: personId,
            nhi: nhi,
            name: editNameInput.value.trim(),
            legal_id: editLegalStatusSelect.value,
            is_special_patient: editSpecialPatientCheckbox.checked,
            has_vnr: editVnrCheckbox.checked,
            special_notes: editSpecialNotesTextarea.value.trim()
        };

        try {
            const response = await fetch(`/api/people/edit`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(personData)
            });
            if (response.ok) {
                alert('Details updated successfully');
                window.location.href = '/main-editor';
            } else {
                alert('Error updating details');
            }
        } catch (error) {
            console.error('Error updating details:', error);
        }
    });
    
    saveAssignmentsBtn.addEventListener('click', async () => {
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
            const response = await fetch(`/api/people/${personId}/assignments`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(assignmentData)
            });

            if (response.ok) {
                alert('Assignments saved successfully!');
                window.location.href = '/main-editor';
            } else {
                alert('Failed to save assignments.');
            }
        } catch (error) {
            console.error('Error saving assignments:', error);
        }
    });

    moveSubmitBtn.addEventListener('click', async () => {
        const moveData = {
            personId: personId,
            destinationRoom: moveRoomSelect.value
        };

        try {
            const response = await fetch('/api/people/move', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(moveData)
            });

            if (response.ok) {
                alert('Person moved successfully');
                window.location.href = '/main-editor';
            } else {
                alert('Error moving person');
            }
        } catch (error) {
            console.error('Error moving person:', error);
        }
    });

    removePersonBtn.addEventListener('click', async () => {
        if (!currentPerson) {
            alert("No person selected.");
            return;
        }
        const confirmation = confirm(`Are you sure you want to remove ${currentPerson.name} from room ${currentPerson.room}? This action cannot be undone.`);
        if (confirmation) {
            try {
                const response = await fetch(`/api/people/remove/${currentPerson.id}`, {
                    method: 'DELETE'
                });
                if (response.ok) {
                    alert(`${currentPerson.name} has been removed successfully.`);
                    window.location.href = '/main-editor';
                } else {
                    const errorData = await response.json();
                    alert(`Failed to remove person: ${errorData.error}`);
                }
            } catch (error) {
                console.error('Error removing person:', error);
                alert('An error occurred while trying to remove the person.');
            }
        }
    });

    // Assignment button listeners
    assignCmBtn.addEventListener('click', () => moveSelectedOptions(availableStaffList, casemanagerList, 2));
    removeCmBtn.addEventListener('click', () => moveSelectedOptions(casemanagerList, availableStaffList, null));
    assignAssocBtn.addEventListener('click', () => moveSelectedOptions(availableStaffList, associateList, 2));
    removeAssocBtn.addEventListener('click', () => moveSelectedOptions(associateList, availableStaffList, null));

    // --- Start the App ---
    initialize();
});