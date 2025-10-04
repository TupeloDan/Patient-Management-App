document.addEventListener('DOMContentLoaded', () => {
    const availableStaffList = document.getElementById('available-staff-list');
    const delegatedStaffList = document.getElementById('delegated-staff-list');
    const assignDelegatedBtn = document.getElementById('assign-delegated');
    const removeDelegatedBtn = document.getElementById('remove-delegated');
    const saveDelegatedBtn = document.getElementById('save-delegated-btn');
    const staffSelect = document.getElementById('staff-select');
    const staffIdInput = document.getElementById('staff-id');
    const staffNameInput = document.getElementById('staff-name');
    const staffRoleSelect = document.getElementById('staff-role-select');
    const saveStaffBtn = document.getElementById('save-staff-btn');
    const clearStaffFormBtn = document.getElementById('clear-staff-form-btn');

    let allStaff = [];
    let allRoles = [];
    let delegatedStaff = [];
    const delegatableRoles = ["RN", "ACNM", "Charge Nurse", "CNS"];

    async function initialize() {
        try {
            const [staffRes, rolesRes, delegatedRes] = await Promise.all([
                fetch('/api/staff'),
                fetch('/api/roles'),
                fetch('/api/delegated-staff')
            ]);
            allStaff = await staffRes.json();
            allRoles = await rolesRes.json();
            delegatedStaff = await delegatedRes.json();
            populateForms();
        } catch (error) {
            console.error("Failed to initialize staff management page:", error);
        }
    }

    function populateForms() {
        const delegatedIds = new Set(delegatedStaff.map(s => s.ID));
        availableStaffList.innerHTML = '';
        delegatedStaffList.innerHTML = '';
        const staffForDelegation = allStaff.filter(staff => delegatableRoles.includes(staff.Role));

        staffForDelegation.forEach(staff => {
            const option = document.createElement('option');
            option.value = staff.ID;
            option.textContent = `${staff.StaffName} (${staff.Role})`;
            if (delegatedIds.has(staff.ID)) {
                delegatedStaffList.appendChild(option);
            } else {
                availableStaffList.appendChild(option);
            }
        });

        staffSelect.innerHTML = '<option value="">Select a staff member to edit...</option>';
        allStaff.sort((a, b) => a.StaffName.localeCompare(b.StaffName)).forEach(staff => {
            const option = document.createElement('option');
            option.value = staff.ID;
            option.textContent = `${staff.StaffName} (${staff.Role})`;
            staffSelect.appendChild(option);
        });

        staffRoleSelect.innerHTML = '<option value="">Select a role...</option>';
        allRoles.forEach(role => {
            const option = document.createElement('option');
            option.value = role.ID;
            option.textContent = role.Role;
            staffRoleSelect.appendChild(option);
        });
    }

    function moveSelectedOptions(source, dest) {
        Array.from(source.selectedOptions).forEach(option => dest.appendChild(option));
    }

    function clearStaffEditForm() {
        staffSelect.value = '';
        staffIdInput.value = '';
        staffNameInput.value = '';
        staffRoleSelect.value = '';
        saveStaffBtn.textContent = 'Save New Staff';
    }

    assignDelegatedBtn.addEventListener('click', () => moveSelectedOptions(availableStaffList, delegatedStaffList));
    removeDelegatedBtn.addEventListener('click', () => moveSelectedOptions(delegatedStaffList, availableStaffList));

    saveDelegatedBtn.addEventListener('click', async () => {
        const delegatedIds = Array.from(delegatedStaffList.options).map(opt => Number(opt.value));
        try {
            const response = await fetch('/api/delegated-staff/update', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ staff_ids: delegatedIds })
            });
            if (response.ok) {
                alert('Delegated staff list updated successfully.');
            } else {
                alert('Failed to update delegated staff.');
            }
        } catch (error) {
            console.error('Error saving delegated staff:', error);
        }
    });

    staffSelect.addEventListener('change', () => {
        const selectedId = staffSelect.value;
        if (!selectedId) {
            clearStaffEditForm();
            return;
        }
        
        const staffMember = allStaff.find(s => s.ID == selectedId);
        if (staffMember) {
            staffIdInput.value = staffMember.ID;
            staffNameInput.value = staffMember.StaffName;
            staffRoleSelect.value = staffMember.RoleID;
            saveStaffBtn.textContent = 'Save Changes';
        }
    });

    clearStaffFormBtn.addEventListener('click', clearStaffEditForm);

    saveStaffBtn.addEventListener('click', async () => {
        const staffId = staffIdInput.value;
        const staffName = staffNameInput.value.trim();
        const roleId = staffRoleSelect.value;
        if (!staffName || !roleId) {
            alert("Please provide a name and select a role.");
            return;
        }

        const isUpdating = !!staffId;
        const url = isUpdating ? `/api/staff/update/${staffId}` : '/api/staff/add';
        const method = isUpdating ? 'PUT' : 'POST';

        try {
            const response = await fetch(url, {
                method: method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: staffName, role_id: roleId })
            });
            if (response.ok) {
                alert(`Staff member ${isUpdating ? 'updated' : 'added'} successfully.`);
                clearStaffEditForm();
                await initialize();
            } else {
                alert('Failed to save staff member.');
            }
        } catch (error) {
            console.error('Error saving staff member:', error);
        }
    });
    initialize();
});