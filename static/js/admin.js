document.addEventListener('DOMContentLoaded', () => {
    // --- Common Elements ---
    const expiryDatePicker = flatpickr("#expiry-date", { dateFormat: "d/m/Y" });

    // --- UI Text Editor Elements ---
    const contextSelect = document.getElementById('context-select');
    const textFieldsContainer = document.getElementById('text-fields-container');
    const textActionsContainer = document.getElementById('actions-container');
    const saveTextBtn = document.getElementById('save-text-btn');
    const closeTextEditorBtn = document.getElementById('close-text-editor-btn');

    // --- Manage Notice Elements ---
    const noticeSelect = document.getElementById('notice-select');
    const noticeIdInput = document.getElementById('notice-id');
    const noticeTextInput = document.getElementById('notice-text');
    const addNoticeBtn = document.getElementById('add-notice-btn');
    const saveNoticeBtn = document.getElementById('save-notice-btn');
    const deleteNoticeBtn = document.getElementById('delete-notice-btn');
    const clearNoticeFormBtn = document.getElementById('clear-notice-form-btn');

    // --- Cleanup Elements ---
    const clearLeaveReturnsBtn = document.getElementById('clear-leave-returns-btn');

    let allNotices = [];

    // --- Main Initialization ---
    async function initialize() {
        // This function now specifically loads the notices for the editor
        await loadAllNoticesForEditor();
    }

    async function loadAllNoticesForEditor() {
        try {
            // THIS IS THE FIX: The script now calls the correct '/api/notices/all' endpoint.
            const response = await fetch('/api/notices/all');
            if (!response.ok) {
                throw new Error('Failed to fetch the list of all notices.');
            }
            allNotices = await response.json();
            populateNoticeSelector();
        } catch (error) {
            console.error("Failed to load notices for editor:", error);
            alert("Error: Could not load the list of notices to edit.");
        }
    }

    function populateNoticeSelector() {
        noticeSelect.innerHTML = '<option value="">--- Create New Notice ---</option>';
        allNotices.forEach(notice => {
            const option = document.createElement('option');
            option.value = notice.NoticeID;
            const displayText = notice.NoticeText.length > 80 ? notice.NoticeText.substring(0, 80) + '...' : notice.NoticeText;
            option.textContent = displayText;
            noticeSelect.appendChild(option);
        });
    }
    
    function clearNoticeForm() {
        noticeSelect.value = '';
        noticeIdInput.value = '';
        noticeTextInput.value = '';
        expiryDatePicker.clear();
        addNoticeBtn.classList.remove('hidden');
        saveNoticeBtn.classList.add('hidden');
        deleteNoticeBtn.classList.add('hidden');
    }

    // --- UI Text Editor Logic (unchanged) ---
    function closeTextEditor() {
        textFieldsContainer.classList.add('hidden');
        textActionsContainer.classList.add('hidden');
        contextSelect.value = '';
    }

    contextSelect.addEventListener('change', async () => {
        const context = contextSelect.value;
        if (!context) {
            closeTextEditor();
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
                closeTextEditor();
            } else {
                alert('Failed to update text.');
            }
        } catch (error) {
            console.error('Error saving UI text:', error);
        }
    });

    closeTextEditorBtn.addEventListener('click', closeTextEditor);

    // --- Manage Notice Logic ---
    noticeSelect.addEventListener('change', () => {
        const selectedId = noticeSelect.value;
        if (!selectedId) {
            clearNoticeForm();
            return;
        }
        const notice = allNotices.find(n => n.NoticeID == selectedId);
        if (notice) {
            noticeIdInput.value = notice.NoticeID;
            noticeTextInput.value = notice.NoticeText;
            // Use the date from the server to set the date picker
            expiryDatePicker.setDate(notice.ExpiryDate, true, 'Y-m-d H:i:s');
            addNoticeBtn.classList.add('hidden');
            saveNoticeBtn.classList.remove('hidden');
            deleteNoticeBtn.classList.remove('hidden');
        }
    });

    clearNoticeFormBtn.addEventListener('click', clearNoticeForm);

    addNoticeBtn.addEventListener('click', async () => {
        const noticeText = noticeTextInput.value.trim();
        const expiryDate = expiryDatePicker.selectedDates[0];
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
                clearNoticeForm();
                await loadAllNoticesForEditor();
            } else {
                alert('Failed to add notice.');
            }
        } catch (error) {
            console.error('Error adding notice:', error);
        }
    });

    saveNoticeBtn.addEventListener('click', async () => {
        const noticeId = noticeIdInput.value;
        const noticeText = noticeTextInput.value.trim();
        const expiryDate = expiryDatePicker.selectedDates[0];
        if (!noticeId || !noticeText || !expiryDate) {
            alert("All fields are required to save changes.");
            return;
        }
        const formattedDate = flatpickr.formatDate(expiryDate, "d/m/Y");
        try {
            const response = await fetch(`/api/notices/update/${noticeId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ notice_text: noticeText, expiry_date: formattedDate })
            });
            if (response.ok) {
                alert('Notice updated successfully!');
                clearNoticeForm();
                await loadAllNoticesForEditor();
            } else {
                alert('Failed to update notice.');
            }
        } catch (error) {
            console.error('Error updating notice:', error);
        }
    });

    deleteNoticeBtn.addEventListener('click', async () => {
        const noticeId = noticeIdInput.value;
        if (!noticeId) {
            alert("No notice selected to delete.");
            return;
        }
        if (!confirm("Are you sure you want to delete this notice?")) {
            return;
        }
        try {
            const response = await fetch(`/api/notices/delete/${noticeId}`, {
                method: 'DELETE'
            });
            if (response.ok) {
                alert('Notice deleted successfully!');
                clearNoticeForm();
                await loadAllNoticesForEditor();
            } else {
                alert('Failed to delete notice.');
            }
        } catch (error) {
            console.error('Error deleting notice:', error);
        }
    });
    
    // --- Cleanup Logic (unchanged) ---
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
    
    // --- Initialize Page ---
    initialize();
});