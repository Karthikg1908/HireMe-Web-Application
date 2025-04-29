document.addEventListener('DOMContentLoaded', function () {
    const createJobForm = document.getElementById('createJobForm');
    const urlParams = new URLSearchParams(window.location.search);
    const jobId = urlParams.get('job_id');
  
    // If editing, fetch existing job data
    if (jobId) {
      fetch(`/api/job/${jobId}`)
        .then(response => response.json())
        .then(job => {
          if (job) {
            document.getElementById('jobRole').value = job.job_role || '';
            document.getElementById('company').value = job.company || '';
            document.getElementById('package').value = job.package || '';
            document.getElementById('jobDescription').value = job.job_description || '';
          }
        })
        .catch(error => {
          console.error('Error fetching job data:', error);
          alert('Could not load job details.');
        });
    }
  
    // Form submission
    createJobForm.addEventListener('submit', function (event) {
      event.preventDefault();
  
      const jobData = {
        job_role: document.getElementById('jobRole').value,
        company: document.getElementById('company').value,
        package: document.getElementById('package').value,
        job_description: document.getElementById('jobDescription').value
      };
  
      const method = jobId ? 'PUT' : 'POST';
      const endpoint = jobId ? `/api/job/${jobId}` : '/api/job';
  
      fetch(endpoint, {
        method: method,
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(jobData)
      })
        .then(response => response.json())
        .then(data => {
          console.log('Server response:', data);
          if (data.success || data.id) {
            alert(jobId ? 'Job updated successfully' : 'Job created successfully');
            window.location.href = '/recruiter_home';
          } else {
            alert('Failed to save job. Server did not respond with success.');
          }
        })
        .catch(error => {
          console.error('Error submitting job:', error);
          alert('Error occurred while saving the job');
        });
    });
  });
  
  