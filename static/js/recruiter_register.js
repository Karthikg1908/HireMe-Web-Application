// Event listener for form submission
document.getElementById('recruiter_register').addEventListener('submit', function(event) {
  // Prevent the default form submission behavior
  event.preventDefault();

  // Create an object with form data
  const formData = {
    username: document.getElementById('username').value,
    firstname: document.getElementById('firstname').value,
    lastname: document.getElementById('lastname').value,
    email: document.getElementById('email').value,
    password: document.getElementById('password').value,
    confirm_password: document.getElementById('confirm_password').value,
    company: document.getElementById('company').value,
    phone_number: document.getElementById('phone_number').value
  };

  // Make a fetch request to the '/recruiter_register' endpoint
  fetch('/recruiter_register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(formData)
  })
  .then(response => response.json()) // Convert the response to JSON
  .then(data => {
    // Check if the registration was successful and if redirection is required
    if (data.redirected) {
      alert('Recruiter registered successfully!');
      window.location.href = data.url; // Redirect to the provided URL
    } else {
      alert('Error: ' + data.message); // Display error message
    }
  })
  .catch(error => {
    // Handle any errors that occur during the fetch request
    console.error('Error:', error);
    alert('An unexpected error occurred. Please try again.');
  });
});
