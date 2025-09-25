document.addEventListener('DOMContentLoaded', () => {

    // --- API Endpoints ---
    const WHITEBOARD_API = '/data';
    const NOTICES_API = '/api/notices';
    const ONLEAVE_API = '/api/onleave';

    // --- HELPER FUNCTION: This is the definitive parser for your time format ---
    const parseTimeValue = (timeValue) => {
        if (!timeValue) return null;
        const timeString = timeValue.toString();
        // Handles ISO 8601 format from the database which is the most reliable
        if (timeString.includes('T') || timeString.includes(':')) {
            const date = new Date(timeString);
            return !isNaN(date.getTime()) ? date : null;
        } 
        // Fallback for "HHmm" format
        else if (timeString.length >= 4) {
            const hours = parseInt(timeString.substring(0, 2), 10);
            const minutes = parseInt(timeString.substring(2, 4), 10);
            if (isNaN(hours) || isNaN(minutes)) return null;
            const date = new Date();
            date.setHours(hours, minutes, 0, 0);
            return date;
        }
        return null;
    };

    // --- DATA LOADING FUNCTIONS ---

    function loadNotices() {
        const noticesList = document.getElementById('notices-list');
        if (!noticesList) return;

        fetch(NOTICES_API)
            .then(response => response.json())
            .then(notices => {
                noticesList.innerHTML = ''; 
                if (notices.length === 0) {
                    noticesList.innerHTML = '<li>No active notices.</li>';
                } else {
                    notices.forEach(noticeText => {
                        const listItem = document.createElement('li');
                        listItem.textContent = noticeText;
                        noticesList.appendChild(listItem);
                    });
                }
            })
            .catch(error => {
                console.error('Error fetching notices:', error);
                noticesList.innerHTML = '<li>Could not load notices.</li>';
            });
    }

    function loadOnLeaveData() {
        const onLeaveListDiv = document.getElementById('on-leave-list');
        if (!onLeaveListDiv) return;

        fetch(ONLEAVE_API)
            .then(response => response.json())
            .then(data => {
                onLeaveListDiv.innerHTML = '';
                if (data.length === 0) {
                    onLeaveListDiv.innerHTML = '<p>No one is currently on leave.</p>';
                } else {
                    data.forEach(leave => {
                        const entryDiv = document.createElement('div');
                        entryDiv.classList.add('leave-entry');
                        const infoLine = document.createElement('p');
                        infoLine.innerHTML = `<strong>${leave.personName || ''}</strong> (${leave.leaveType || ''}) Staff: ${leave.staffName || ''} Contact: ${leave.contactPhone || ''}`;
                        const descLine = document.createElement('p');
                        descLine.classList.add('leave-description');
                        descLine.textContent = `Description: ${leave.description || ''}`;
                        entryDiv.appendChild(infoLine);
                        entryDiv.appendChild(descLine);
                        onLeaveListDiv.appendChild(entryDiv);
                    });
                }
            })
            .catch(error => {
                console.error('Error fetching on-leave data:', error);
                onLeaveListDiv.innerHTML = '<p>Could not load on-leave information.</p>';
            });
    }

    async function refreshWhiteboard() {
        try {
            const response = await fetch(WHITEBOARD_API);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const data = await response.json();
            
            const whiteboardBody = document.getElementById('whiteboard-body');
            if (!whiteboardBody) return;
           
            whiteboardBody.innerHTML = '';

            data.forEach(person => {
                const row = document.createElement('tr');
                
                const formatDate = (d) => d ? new Date(d).toLocaleDateString() : '';
                const dueTimeObject = parseTimeValue(person.LeaveReturn);
                const formattedTime = dueTimeObject ? dueTimeObject.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : '';
                
                const percentValue = person['Progress%'] || 0;
                let dataBarHtml = '';
                if (percentValue > 0) {
                    dataBarHtml = `
                        <div class="data-bar-container">
                            <div class="data-bar-fill" style="width: ${percentValue * 100}%;"></div>
                            <div class="data-bar-text">${(percentValue * 100).toFixed(0)}%</div>
                        </div>
                    `;
                }

                row.innerHTML = `
                    <td>${person.Room || ''}</td>
                    <td>${person.NHI || ''}</td>
                    <td>${person.PersonName || ''}</td>
                    <td>${person.Legal || ''}</td>
                    <td>${person.HasVNR ? 'VNR' : ''}</td>
                    <td>${formatDate(person.TreatmentPlans)}</td>
                    <td>${formatDate(person.HoNos)}</td>
                    <td>${formatDate(person['UDSDue'])}</td>
                    <td></td><td></td><td></td><td></td><td></td>
                    <td>${person['UDSFrequency'] || ''}</td>
                    <td>${person['MDTDay'] || ''}</td>
                    <td>${formattedTime}</td>
                    <td>${dataBarHtml}</td>
                    <td>${person.ClinicianName || ''}</td>
                    <td>${person.CaseManagers || ''}</td>
                    <td>${person.Associates || ''}</td>
                    <td>${person.SpecialNotes || ''}</td>
                    
                   
                `;
                
                whiteboardBody.appendChild(row);

                // --- APPLY ALL CONDITIONAL FORMATTING ---

                if (person.IsSpecialPatient) {
                    row.cells[2].classList.add('font-alert-red');
                    row.cells[3].classList.add('font-alert-red');
                }

                if (person.HasVNR) {
                    row.cells[4].classList.add('font-alert-red');
                }

                const taskData = [person['RelSecurity'], person.Profile, person.Bloods, person.Metobolic, person['FlightRisk']];
                [8, 9, 10, 11, 12].forEach((colIndex, i) => {
                    if (person.NHI) {
                        row.cells[colIndex].classList.add(taskData[i] ? 'task-done' : 'task-not-done');
                    }
                });
                
                const today = new Date();
                today.setHours(0, 0, 0, 0);
                const dateFields = { 5: person.TreatmentPlans, 6: person.HoNos, 7: person['UDSDue'] };
                for (const colIndex in dateFields) {
                    const dateValue = dateFields[colIndex];
                    if (dateValue && new Date(dateValue) < today) {
                        row.cells[colIndex].classList.add('date-overdue');
                    }
                }

                if (dueTimeObject) {
                    const currentTime = new Date();
                    if (currentTime > dueTimeObject) {
                        [0, 1, 15].forEach(i => row.cells[i].classList.add('font-alert-orange'));
                    } else {
                        [0, 1, 15].forEach(i => row.cells[i].classList.add('font-alert-yellow'));
                    }
                }
            });

        } catch (error) {
            console.error('Error refreshing whiteboard:', error);
        }
    }
    
    // --- INITIAL LOAD AND REFRESH INTERVALS ---
    refreshWhiteboard();
    loadNotices();
    loadOnLeaveData();
    
    setInterval(refreshWhiteboard, 5000);
    setInterval(loadNotices, 15000); 
    setInterval(loadOnLeaveData, 5000);
});