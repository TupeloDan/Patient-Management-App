document.addEventListener('DOMContentLoaded', () => {
    const contextSelect = document.getElementById('context-select');
    const textFieldsContainer = document.getElementById('text-fields-container');
    const actionsContainer = document.getElementById('actions-container');
    const saveChangesBtn = document.getElementById('save-changes-btn');

    contextSelect.addEventListener('change', async () => {
        const context = contextSelect.value;
        if (!context) {
            textFieldsContainer.innerHTML = '';
            textFieldsContainer.classList.add('hidden');
            actionsContainer.classList.add('hidden');
            return;
        }

        try {
            const response = await fetch(`/api/ui-text?context=${context}`);
            const textData = await response.json();
            
            // THIS IS THE DEBUGGING LINE
            console.log("Data received from server:", textData);

            textFieldsContainer.innerHTML = ''; // Clear previous fields
            
            // Check if the received data is empty
            if (Object.keys(textData).length === 0) {
                textFieldsContainer.innerHTML = '<p>No text fields found for this context.</p>';
            } else {
                for (const controlName in textData) {
                    const captionText = textData[controlName];

                    const formGroup = document.createElement('div');
                    formGroup.className = 'form-group';

                    const label = document.createElement('label');
                    label.textContent = controlName;
                    label.htmlFor = controlName;

                    const input = document.createElement('textarea');
                    input.id = controlName;
                    input.className = 'text-input';
                    input.dataset.controlName = controlName; // Store the key
                    input.value = captionText;
                    input.rows = 2;

                    formGroup.appendChild(label);
                    formGroup.appendChild(input);
                    textFieldsContainer.appendChild(formGroup);
                }
            }

            textFieldsContainer.classList.remove('hidden');
            actionsContainer.classList.remove('hidden');

        } catch (error) {
            console.error('Error fetching UI text:', error);
            alert('Could not load text fields for editing.');
        }
    });

    saveChangesBtn.addEventListener('click', async () => {
        const context = contextSelect.value;
        const updates = {};
        const inputs = textFieldsContainer.querySelectorAll('.text-input');

        inputs.forEach(input => {
            const controlName = input.dataset.controlName;
            const newText = input.value;
            updates[controlName] = newText;
        });

        if (Object.keys(updates).length === 0) {
            alert("No text fields to update.");
            return;
        }

        try {
            const response = await fetch('/api/ui-text/update', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ context, updates })
            });

            if (response.ok) {
                alert('UI text updated successfully!');
            } else {
                const errorData = await response.json();
                alert(`Failed to update text: ${errorData.error}`);
            }
        } catch (error) {
            console.error('Error saving UI text:', error);
            alert('An error occurred while saving the changes.');
        }
    });
});