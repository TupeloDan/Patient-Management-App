// static/js/api.js

const API_BASE = ''; // We can use relative paths

async function fetchData(url) {
    const response = await fetch(`${API_BASE}${url}`);
    if (!response.ok) {
        throw new Error(`Network response was not ok for ${url}`);
    }
    return response.json();
}

async function updateData(url, method, body) {
    const response = await fetch(`${API_BASE}${url}`, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    });
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Update failed.');
    }
    return response.json();
}

export const patientApi = {
    getAll: () => fetchData('/api/people'),
    getLeaves: (patientId) => fetchData(`/api/people/${patientId}/leaves`),
    updateField: (patientId, fieldName, newValue) => updateData(`/api/people/${patientId}/update-field`, 'PATCH', { field_name: fieldName, new_value: newValue }),
    updatePlanDate: (patientId, date) => updateData(`/api/people/${patientId}/update-plan-date`, 'POST', { completed_date: date }),
    updateHonosDate: (patientId, date) => updateData(`/api/people/${patientId}/update-honos-date`, 'POST', { completed_date: date }),
    updateUdsDate: (patientId, date) => updateData(`/api/people/${patientId}/update-uds-date`, 'POST', { last_test_date: date })
};

export const staffApi = {
    getAll: () => fetchData('/api/staff')
};

export const uiTextApi = {
    getContext: (context) => fetchData(`/api/ui-text?context=${context}`)
};