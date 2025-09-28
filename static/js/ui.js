// static/js/ui.js
const UDS_OPTIONS = ['Weekly', 'Bi-Weekly', 'Monthly', 'Random', 'OnRequest'];
const MDT_DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];

const formatDate = (dateString) => {
    if (!dateString) return '--';
    const date = new Date(dateString);
    if (isNaN(date)) return '--';
    return date.toLocaleDateString('en-NZ');
};

export function initializeDatePicker(selector) {
    return flatpickr(selector, { dateFormat: "d/m/Y" });
}

export function initializeChoices(selectors) {
    const instances = {};
    for (const key in selectors) {
        if (selectors[key]) {
            instances[key] = new Choices(selectors[key], {
                removeItemButton: true,
                searchResultLimit: 10
            });
        }
    }
    return instances;
}

export function renderPatientList(container, patients, onSelectCallback) {
    if (!container) return;
    container.innerHTML = '';
    patients.forEach(person => {
        if (person.nhi) {
            const item = document.createElement('div');
            item.className = 'patient-list-item';
            item.dataset.patientId = person.id;
            item.innerHTML = `<strong>${person.name}</strong><br><small>${person.nhi} - Room: ${person.room}</small>`;
            item.addEventListener('click', () => onSelectCallback(person.id));
            container.appendChild(item);
        }
    });
}

export function populateDetailsPane(patient, elements) {
    elements.lastPlanDate.textContent = formatDate(patient.last_treatment_plan);
    elements.planDueDate.textContent = formatDate(patient.treatment_plans_due);
    elements.lastHonosDate.textContent = formatDate(patient.last_honos);
    elements.honosDueDate.textContent = formatDate(patient.honos_due);
    elements.lastUdsDate.textContent = formatDate(patient.last_uds);
    elements.udsDueDate.textContent = formatDate(patient.uds_due);
    elements.udsFrequencySelect.innerHTML = UDS_OPTIONS.map(o => `<option value="${o}" ${patient.uds_frequency === o ? 'selected' : ''}>${o}</option>`).join('');
    elements.mdtDaySelect.innerHTML = MDT_DAYS.map(d => `<option value="${d}" ${patient.mdt_day === d ? 'selected' : ''}>${d}</option>`).join('');
    for (const taskName in elements.taskToggles) {
        const btn = elements.taskToggles[taskName];
        if (btn) {
            const isDone = patient[taskName];
            btn.textContent = isDone ? 'Done' : 'Not Done';
            btn.className = 'task-toggle-btn';
            btn.classList.add(isDone ? 'done' : 'not-done');
        }
    }
}

export function populateLeaveLists(listElements, leaves, onSelectCallback) {
    listElements.leavesTodayList.innerHTML = '';
    listElements.allLeavesList.innerHTML = '';
    if (!leaves || leaves.length === 0) {
        listElements.leavesTodayList.innerHTML = '<div class="leave-item">No leaves recorded.</div>';
        return;
    }
    const today = new Date().toLocaleDateString('en-NZ');
    leaves.forEach(leave => {
        const item = document.createElement('div');
        item.className = 'leave-item';
        item.addEventListener('click', () => onSelectCallback(leave, item));
        const leaveDate = new Date(leave.LeaveDate).toLocaleDateString('en-NZ');
        const leaveTime = leave.LeaveTime ? new Date(leave.LeaveTime).toLocaleTimeString('en-NZ', { hour: '2-digit', minute: '2-digit' }) : '';
        const returnTime = leave.ReturnTime ? new Date(leave.ReturnTime).toLocaleTimeString('en-NZ', { hour: '2-digit', minute: '2-digit' }) : 'N/A';
        item.textContent = `${leaveDate} | ${leaveTime} - ${returnTime} | ${leave.LeaveType}`;
        if (leaveDate === today) {
            listElements.leavesTodayList.appendChild(item);
        }
        else {
            listElements.allLeavesList.appendChild(item);
        }
    });
}

export function highlightPatient(patientId) {
    document.querySelectorAll('.patient-list-item').forEach(item => {
        item.classList.toggle('selected', item.dataset.patientId == patientId);
    });
}

export function showDetailsPane(patient, elements) {
    elements.detailsPane.classList.remove('hidden');
    elements.detailsHeader.textContent = `Currently Managing: ${patient.name}`;
    elements.detailsPane.classList.toggle('is-special', patient.is_special_patient);
    populateDetailsPane(patient, elements);
}

export function highlightLeave(leaveElement) {
    document.querySelectorAll('.leave-item').forEach(item => item.classList.remove('selected'));
    leaveElement.classList.add('selected');
}