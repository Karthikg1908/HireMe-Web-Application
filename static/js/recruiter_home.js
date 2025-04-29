document.addEventListener('DOMContentLoaded', function () {
  // Handle the reports button click
  const report = document.getElementById('reports');
  if (report) {
    report.addEventListener('click', function (event) {
      event.preventDefault();
      window.location.href = '/report'; // Redirect to the report page
    });
  }

  // Fetch & Populate Job Table
  fetch('/api/jobs')
    .then(response => response.json())
    .then(data => {
      const jobsTable = document.getElementById('jobsTable').getElementsByTagName('tbody')[0];

      data.forEach(job => {
        const row = jobsTable.insertRow();
        row.insertCell(0).textContent = job[0]; // Job ID
        row.insertCell(1).textContent = job[1]; // Job Role
        row.insertCell(2).textContent = job[2]; // Company
        row.insertCell(3).textContent = job[3]; // Package

        // View Button - index 4
        const viewCell = row.insertCell(4);
        viewCell.classList.add('description');
        const viewButton = document.createElement('button');
        viewButton.classList.add('view-btn');
        viewButton.textContent = 'View';
        viewButton.onclick = () => {
          window.location.href = `/recruiter/job/${job[0]}`;
        };
        viewCell.appendChild(viewButton);

        // Status Cell - index 5
        const statusCell = row.insertCell(5);
        statusCell.textContent = job[4] === 'closed' ? '❌ Closed' : '✅ Open';
        if (job[4] === 'closed') {
          row.classList.add('closed-job');
        }

        // Reopen/Close Button - index 6
        const toggleStatusCell = row.insertCell(6);
        toggleStatusCell.classList.add('description');
        const toggleStatusButton = document.createElement('button');
        toggleStatusButton.textContent = job[4] === 'closed' ? 'Reopen' : 'Close';
        toggleStatusButton.classList.add('toggle-status-btn');
        toggleStatusButton.onclick = () => {
          const newStatus = job[4] === 'closed' ? 'open' : 'closed';

          fetch(`/api/job/${job[0]}/status`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ status: newStatus })
          })
            .then(response => response.json())
            .then(data => {
              if (data.success) {
                location.reload(); // Reload the table to reflect changes
              } else {
                alert('Failed to update status');
              }
            });
        };
        toggleStatusCell.appendChild(toggleStatusButton);

        // Action Buttons (Edit + Delete) - index 7
        const actionCell = row.insertCell(7);
        actionCell.classList.add('description');

        // Edit Button
        const editButton = document.createElement('button');
        editButton.classList.add('edit-btn');
        editButton.textContent = 'Edit';
        editButton.onclick = () => {
          window.location.href = `/create_job_page?job_id=${job[0]}`;
        };
        actionCell.appendChild(editButton);

        // Delete Button
        const deleteButton = document.createElement('button');
        deleteButton.classList.add('delete-btn');
        deleteButton.textContent = 'Delete';
        deleteButton.style.marginLeft = '10px';
        deleteButton.onclick = () => {
          if (confirm('Are you sure you want to delete this job?')) {
            fetch(`/api/job/${job[0]}`, {
              method: 'DELETE'
            }).then(res => {
              if (res.ok) {
                row.remove();
              } else {
                alert('Failed to delete job.');
              }
            });
          }
        };
        actionCell.appendChild(deleteButton);
      });
    });

  // Create Job Button
  const createJobBtn = document.getElementById('create-job-btn');
  if (createJobBtn) {
    createJobBtn.addEventListener('click', function () {
      window.location.href = '/create_job_page'; // Redirect to the job creation page
    });
  }

  // Logout Button
  document.getElementById('logout-btn').addEventListener('click', function() { 
    fetch('/logout_rec')
.then(() => {
  window.location.href = '/';
}).catch(error => console.error('Error logging out:', error));
  });
});

