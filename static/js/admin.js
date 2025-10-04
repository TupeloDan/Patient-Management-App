document.addEventListener('DOMContentLoaded', () => {
    // --- Common Elements ---
    const datePicker = flatpickr("#expiry-date", { dateFormat: "d/m/Y" });

    // --- UI Text Editor Elements ---
    const contextSelect = document.getElementById('context-select');
    const textFieldsContainer = document.getElementById('text-fields-container');
    const textActionsContainer = document.getElementById('actions-container');
    const saveTextBtn = document.getElementById('save-text-btn');

    // --- Add Notice Elements ---
    const noticeTextInput = document.getElementById('notice-text');
    const addNoticeBtn = document.getElementById('add-notice-btn');

    // --- Cleanup Elements ---
    const clearLeaveReturnsBtn = document.getElementById('clear-leave-returns-btn');

    // --- UI Text Editor Logic ---
    contextSelect.addEventListener('change', async () => {
        const context = contextSelect.value;
        if (!context) {
            textFieldsContainer.innerHTML = '';
            textFieldsContainer.classList.add('hidden');
            textActionsContainer.classList.add('hidden');
            return;
        }

        try {
            const response = await fetch(`/api/ui-text?context=${context}`);
            const textData = await response.json();
            
            textFieldsContainer.innerHTML = '';
            
            for (const controlName in textData) {
                const formGroup = document.createElement('div');
                formGroup.className = 'form-group';
                const label = document.createElement('label');
                label.textContent = controlName;
                const input = document.createElement('textarea');
                input.className = 'text-input';
                input.dataset.controlName = controlName;
                input.value = textData[controlName];
                input.rows = 2;
                formGroup.appendChild(label);
                formGroup.appendChild(input);
                textFieldsContainer.appendChild(formGroup);
            }

            textFieldsContainer.classList.remove('hidden');
            textActionsContainer.classList.remove('hidden');

        } catch (error) {
            console.error('Error fetching UI text:', error);
            alert('Could not load text fields for editing.');
        }
    });

    saveTextBtn.addEventListener('click', async () => {
        const context = contextSelect.value;
        const updates = {};
        textFieldsContainer.querySelectorAll('.text-input').forEach(input => {
            updates[input.dataset.controlName] = input.value;
        });

        try {
            const response = await fetch('/api/ui-text/update', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ context, updates })
            });
            if (response.ok) {
                alert('UI text updated successfully!');
            } else {
                alert('Failed to update text.');
            }
        } catch (error) {
            console.error('Error saving UI text:', error);
        }
    });

    // --- Add Notice Logic ---
    addNoticeBtn.addEventListener('click', async () => {
        const noticeText = noticeTextInput.value.trim();
        const expiryDate = datePicker.selectedDates[0];

        if (!noticeText || !expiryDate) {
            alert("Please provide both notice text and an expiry date.");
            return;
        }

        const formattedDate = flatpickr.formatDate(expiryDate, "d/m/Y");

        try {
            const response = await fetch('/api/notices/add', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ notice_text: noticeText, expiry_date: formattedDate })
            });

            if (response.ok) {
                alert('Notice added successfully!');
                noticeTextInput.value = '';
                datePicker.clear();
            } else {
                alert('Failed to add notice.');
            }
        } catch (error) {
            console.error('Error adding notice:', error);
        }
    });

    // --- Cleanup Logic ---
    clearLeaveReturnsBtn.addEventListener('click', async () => {
        if (!confirm("Are you sure you want to clear the 'Leave Return' status for ALL patients? This should only be used to fix stuck records.")) {
            return;
        }

        try {
            const response = await fetch('/api/admin/clear-leave-returns', {
                method: 'POST'
            });
            if (response.ok) {
                alert('All leave return statuses have been cleared.');
            } else {
                alert('Failed to clear leave return statuses.');
            }
        } catch (error) {
            console.error('Error clearing leave returns:', error);
        }
    });
});