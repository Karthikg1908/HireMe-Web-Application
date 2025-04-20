document.addEventListener('DOMContentLoaded', function () {
    const createJobForm = document.getElementById('createJobForm');

    createJobForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const jobRole = document.getElementById('jobRole').value;
        const company = document.getElementById('company').value;
        const package = document.getElementById('package').value;
        const jobDescription = document.getElementById('jobDescription').value;

        fetch('/api/jobs', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json' 
            },body: JSON.stringify({  
                job_role: jobRole,
                company: company,
                package: package,
                job_description: jobDescription
            })}) .then(response => response.json())
        .         then(data => { 
            if (data.success) { 
                alert('Job created successfully'); 
                window.location.href = '/recruiter_home'; 
            } else { 
                alert('Failed to create job'); 
            }}) .catch(error => { 
            console.error('Error:', error); 
        }); 
    });
}); 
 