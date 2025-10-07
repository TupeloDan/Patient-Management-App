document.addEventListener('DOMContentLoaded', () => {

    // --- API Endpoints ---
    const WHITEBOARD_API = '/data';
    const NOTICES_API = '/api/notices';
    const ONLEAVE_API = '/api/onleave';

    // --- HELPER FUNCTION ---
    const parseTimeValue = (timeValue) => {
        if (!timeValue) return null;
        const timeString = timeValue.toString();
        if (timeString.includes('T') || timeString.includes(':')) {
            const date = new Date(timeString);
            return !isNaN(date.getTime()) ? date : null;
        }
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

                        // --- NEW LOGIC TO CHECK IF OVERDUE ---
                        if (leave.expectedReturn) {
                            const expectedReturnTime = new Date(leave.expectedReturn);
                            const currentTime = new Date();
                            if (currentTime > expectedReturnTime) {
                                entryDiv.classList.add('overdue-leave');
                            }
                        }
                        // --- END OF NEW LOGIC -

                        // THIS IS THE FIX: We no longer do any date parsing.
                        const leaveTime = leave.leaveTime || 'N/A';
                        
                        infoLine.innerHTML = `<strong>${leave.personName || ''}</strong> (${leave.leaveType || ''}) | Left at: ${leaveTime} for ${leave.duration || '?'} mins<br>
                                            Staff: ${leave.staffName || ''} | Contact: ${leave.contactPhone || ''}`;

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
            const response = await fetch('/data');
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const data = await response.json();

            const whiteboardBody = document.getElementById('whiteboard-body');
            if (!whiteboardBody) return;

            whiteboardBody.innerHTML = '';

            data.forEach(person => {
                const row = document.createElement('tr');

                const formatDate = (d) => d ? new Date(d).toLocaleDateString() : '';
                const dueTimeObject = parseTimeValue(person.leave_return);
                const formattedTime = dueTimeObject ? dueTimeObject.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : '';

                const percentValue = person.progress_percent || 0;
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
                <td>${person.room || ''}</td>
                <td>${person.nhi || ''}</td>
                <td>${person.name || ''}</td>
                <td>${person.legal || ''}</td> 
                <td>${person.has_vnr ? 'VNR' : ''}</td>
                <td>${formatDate(person.treatment_plans_due)}</td>
                <td>${formatDate(person.honos_due)}</td>
                <td>${formatDate(person.uds_due)}</td>
                <td></td><td></td><td></td><td></td><td></td>
                <td>${person.uds_frequency || ''}</td>
                <td>${person.mdt_day || ''}</td>
                <td>${formattedTime}</td>
                <td>${dataBarHtml}</td>
                <td>${person.clinician_name || ''}</td>
                <td>${person.case_managers || ''}</td>
                <td>${person.associates || ''}</td>
                <td>${person.special_notes || ''}</td>
            `;

                whiteboardBody.appendChild(row);

                if (person.is_special_patient) {
                    row.cells[2].classList.add('font-alert-red');
                    row.cells[3].classList.add('font-alert-red');
                }
                if (person.has_vnr) {
                    row.cells[4].classList.add('font-alert-red');
                }
                const taskData = [person.rel_security, person.profile, person.bloods, person.metobolic, person.flight_risk];
                [8, 9, 10, 11, 12].forEach((colIndex, i) => {
                    if (person.nhi) {
                        row.cells[colIndex].classList.add(taskData[i] ? 'task-done' : 'task-not-done');
                    }
                });
                const today = new Date();
                today.setHours(0, 0, 0, 0);
                const dateFields = { 5: person.treatment_plans_due, 6: person.honos_due, 7: person.uds_due };
                for (const colIndex in dateFields) {
                    const dateValue = dateFields[colIndex];
                    if (dateValue && new Date(dateValue) < today) {
                        row.cells[colIndex].classList.add('date-overdue');
                    }
                }
                if (dueTimeObject) {
                    const currentTime = new Date();
                    if (currentTime > dueTimeObject) {
                        [0, 15].forEach(i => row.cells[i].classList.add('font-alert-orange'));
                    } else {
                        [0, 15].forEach(i => row.cells[i].classList.add('font-alert-yellow'));
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