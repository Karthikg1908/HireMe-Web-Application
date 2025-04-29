document.getElementById('student_register').addEventListener('submit', function(event) {
  event.preventDefault();

  const form = document.getElementById('student_register');
  const formData = new FormData(form);  // Automatically collects input values including files

  fetch('/student_register', {
      method: 'POST',
      body: formData  // No need to set Content-Type; browser sets it with proper boundary
  })
  .then(response => response.json())
  .then(data => {
      if (data.redirected) {
          alert('Student registered successfully!');
          window.location.href = data.url;
      } else {
          alert('Error: ' + data.message);
      }
  })
  .catch(error => {
      console.error('Error:', error);
      alert('An unexpected error occurred. Please try again.');
  });
});
