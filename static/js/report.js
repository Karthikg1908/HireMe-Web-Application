document.addEventListener('DOMContentLoaded', () => {

    const reportTable = document.querySelector('#reportTable tbody');
    const backbutton = document.getElementById('back-to-index');
    const logoutButton = document.getElementById('logout-btn'); 

    // Fetching the report data from the backend
    fetch('/api/report')
    .then(response => response.json())
    .then(data => {
        data.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${item.student_name}</td>
                <td>${item.branch}</td>
                <td>${item.job_role}</td>
                <td>${item.company}</td>
                <td>${item.package}</td>
                <td><a href="#" class="view-resume" data-resume="${item.resume}">View Resume</a></td>
                <td class="action-cell">
                    ${item.action === 'Processing' 
                        ? `<button class="btn-selected" data-email="${item.email_id}" data-name="${item.student_name}" data-appid="${item.application_id}">Selected</button>
                        <button class="btn-rejected" data-email="${item.email_id}" data-name="${item.student_name}" data-appid="${item.application_id}">Rejected</button>` 
                        : item.action}
                </td>

            `;
            reportTable.appendChild(row);
        });
    })
    .catch(error => console.error('Error fetching report:', error));

    // Back button functionality
    backbutton.addEventListener('click', function (event) {
        event.preventDefault();  
        window.location.href = '/recruiter_home';  
    });

    // Logout button functionality
    logoutButton.addEventListener('click', function(event) {
        event.preventDefault();
        fetch('/logout_rec')
        .then(() => {
            window.location.href = '/';
        })
        .catch(error => console.error('Error logging out:', error));   
    });

    // Event listener for report table (buttons and resume links)
    reportTable.addEventListener('click', function(event) {
        const target = event.target;

        // View Resume in a small new window
        if (target.classList.contains('view-resume')) {
            event.preventDefault();
            const resumePath = target.dataset.resume;
            window.open(
                `/resumes/${resumePath}`,
                'ResumeWindow',
                'width=800,height=600,scrollbars=yes,resizable=yes'
            );
            return; // stop further processing for this click
        }

        // Handle Selected/Rejected buttons
        if (target.classList.contains('btn-selected') || target.classList.contains('btn-rejected')) {
            const email = target.dataset.email;
            const name = target.dataset.name;
            const row = target.closest('tr');
            const actionCell = row.querySelector('.action-cell');
            const newStatus = target.classList.contains('btn-selected') ? 'Selected' : 'Rejected';
            const templateId = target.classList.contains('btn-selected') 
                ? 'template_v7jph5a' 
                : 'template_qz3whfw';

            // Disable both buttons
            const buttons = actionCell.querySelectorAll('button');
            buttons.forEach(btn => {
                btn.disabled = true;
                btn.innerText = 'Sending...';
            });

            emailjs.send('service_jna8s0g', templateId, {
                name: name,
                email: email
            })
            .then(response => {
                alert(`Email sent to ${name} (${email}) successfully!`);
                
                // Replace buttons with new status
                actionCell.textContent = newStatus;

                const applicationId = parseInt(target.dataset.appid);

                fetch('/api/update_action', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email: email, action: newStatus, application_id: applicationId })
                });

            })
            .catch(error => {
                alert(`Failed to send email to ${name}. Error: ${error.text || error}`);
                console.error('EmailJS error:', error);
                
                // Re-enable buttons on failure
                buttons.forEach(btn => {
                    btn.disabled = false;
                    btn.innerText = btn.classList.contains('btn-selected') ? 'Selected' : 'Rejected';
                });
            });
        }
    });

});
