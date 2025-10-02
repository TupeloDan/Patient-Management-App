document.addEventListener('DOMContentLoaded', () => {
    const actionSelect = document.getElementById('action-select');
    const assignForm = document.getElementById('assign-form');
    const editForm = document.getElementById('edit-form');
    const moveForm = document.getElementById('move-form');

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
    const editPersonSelect = document.getElementById('edit-person-select');
    const editNhiInput = document.getElementById('edit-nhi');
    const editNameInput = document.getElementById('edit-name');
    const editLegalStatusSelect = document.getElementById('edit-legal-status');
    const editSpecialPatientCheckbox = document.getElementById('edit-special-patient');
    const editVnrCheckbox = document.getElementById('edit-vnr');
    const editSpecialNotesTextarea = document.getElementById('edit-special-notes');
    const editSubmitBtn = document.getElementById('edit-submit-btn');

    // Move form elements
    const movePersonSelect = document.getElementById('move-person-select');
    const moveRoomSelect = document.getElementById('move-room-select');
    const moveSubmitBtn = document.getElementById('move-submit-btn');

    let allPeople = [];
    let mhaSections = [];

    async function initialize() {
        await Promise.all([fetchPeople(), fetchMhaSections()]);
        populateDropdowns();
    }

    async function fetchPeople() {
        try {
            const response = await fetch('/api/people');
            allPeople = await response.json();
        } catch (error) {
            console.error('Error fetching people:', error);
        }
    }

    async function fetchMhaSections() {
        try {
            const response = await fetch('/api/mha-sections');
            mhaSections = await response.json();
        } catch (error) {
            console.error('Error fetching MHA sections:', error);
        }
    }

    function populateDropdowns() {
        // Clear existing options
        assignRoomSelect.innerHTML = '<option value="">Select a room...</option>';
        editPersonSelect.innerHTML = '<option value="">Select a person...</option>';
        movePersonSelect.innerHTML = '<option value="">Select a person...</option>';
        moveRoomSelect.innerHTML = '<option value="">Select a room...</option>';
        assignLegalStatusSelect.innerHTML = '<option value="">Select a status...</option>';
        editLegalStatusSelect.innerHTML = '<option value="">Select a status...</option>';

        allPeople.forEach(person => {
            if (!person.nhi) { // Empty rooms
                const option = document.createElement('option');
                option.value = person.room;
                option.textContent = person.room;
                assignRoomSelect.appendChild(option.cloneNode(true));
                moveRoomSelect.appendChild(option);
            } else { // Occupied rooms
                const option = document.createElement('option');
                option.value = person.id;
                option.textContent = `${person.name} (${person.room})`;
                editPersonSelect.appendChild(option.cloneNode(true));
                movePersonSelect.appendChild(option);
            }
        });

        mhaSections.forEach(section => {
            const option = document.createElement('option');
            option.value = section.ID;
            option.textContent = section.LegalStatus;
            assignLegalStatusSelect.appendChild(option.cloneNode(true));
            editLegalStatusSelect.appendChild(option);
        });
    }

    actionSelect.addEventListener('change', () => {
        assignForm.classList.add('hidden');
        editForm.classList.add('hidden');
        moveForm.classList.add('hidden');

        const selectedAction = actionSelect.value;
        if (selectedAction === 'assign') {
            assignForm.classList.remove('hidden');
        } else if (selectedAction === 'edit') {
            editForm.classList.remove('hidden');
        } else if (selectedAction === 'move') {
            moveForm.classList.remove('hidden');
        }
    });

    editPersonSelect.addEventListener('change', () => {
        const selectedPersonId = editPersonSelect.value;
        const person = allPeople.find(p => p.id == selectedPersonId);

        if (person) {
            editNhiInput.value = person.nhi || '';
            editNameInput.value = person.name || '';
            editLegalStatusSelect.value = person.legal_id || '';
            editSpecialPatientCheckbox.checked = person.is_special_patient;
            editVnrCheckbox.checked = person.has_vnr;
            editSpecialNotesTextarea.value = person.special_notes || '';
        } else {
            // Clear the form if no one is selected
            editNhiInput.value = '';
            editNameInput.value = '';
            editLegalStatusSelect.value = '';
            editSpecialPatientCheckbox.checked = false;
            editVnrCheckbox.checked = false;
            editSpecialNotesTextarea.value = '';
        }
    });

    async function validateNhi(nhi, currentId = null) {
        const nhiRegex = /^[A-Z]{3}[0-9]{4}$/;
        if (!nhiRegex.test(nhi)) {
            alert('Invalid NHI format. It must be 3 uppercase letters followed by 4 numbers (e.g., ABC1234).');
            return false;
        }

        // Check if the NHI already exists for a *different* person
        const existingPerson = allPeople.find(p => p.nhi === nhi);
        if (existingPerson && existingPerson.id != currentId) {
            alert('This NHI is already assigned to another person.');
            return false;
        }
        
        return true;
    }

    assignSubmitBtn.addEventListener('click', async () => {
        if (!await validateNhi(assignNhiInput.value.trim().toUpperCase())) return;

        const personData = {
            room: assignRoomSelect.value,
            nhi: assignNhiInput.value.trim().toUpperCase(),
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
        const personId = editPersonSelect.value;
        if (!await validateNhi(editNhiInput.value.trim().toUpperCase(), personId)) return;
        
        const personData = {
            id: personId,
            nhi: editNhiInput.value.trim().toUpperCase(),
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
                alert('Person updated successfully');
                window.location.href = '/main-editor';
            } else {
                alert('Error updating person');
            }
        } catch (error) {
            console.error('Error updating person:', error);
        }
    });

    moveSubmitBtn.addEventListener('click', async () => {
        const moveData = {
            personId: movePersonSelect.value,
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

    initialize();
});