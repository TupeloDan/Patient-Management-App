// static/js/ui.js

// This file will contain all functions that directly touch the HTML (the DOM)
// For now, it's a placeholder. We will move the rendering functions here next.

export function renderPatientList(container, patients, onSelect) {
    container.innerHTML = '';
    patients.forEach(person => {
        if (person.nhi) {
            const item = document.createElement('div');
            item.className = 'patient-list-item';
            item.dataset.patientId = person.id;
            item.innerHTML = `<strong>${person.name}</strong><br><small>${person.nhi} - Room: ${person.room}</small>`;
            item.addEventListener('click', () => onSelect(person.id));
            container.appendChild(item);
        }
    });
}

// We will add populateDetailsPane, populateLeaveLists, etc. to this file.