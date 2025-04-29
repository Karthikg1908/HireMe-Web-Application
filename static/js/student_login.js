document.addEventListener('DOMContentLoaded', function() { 
    const loginForm = document.querySelector('#loginForm'); 
    const signupButton = document.getElementById('signupButton');
    const forgotButton = document.getElementById('forgotButton');
    loginForm.addEventListener('submit', function(event) {
    event.preventDefault();
    const usn = document.getElementById('usn').value;
    const password = document.getElementById('password').value; 
      fetch('/login', {
        method:'POST', 
        headers: {
          'Content-Type': 'application/json', 
        },body: JSON.stringify({ 
          usn: usn, 
          password: password
        })}) .then(response => response.json())
      .then(data => {
         if (data.redirected) {
           localStorage.setItem('usn', usn) 
           window.location.href = data.url; 
         } else{
         alert('Login failed. Please check your credentials.');    
         }}) .catch(error => {  
         console.error('Error:', error);
      })}) 
      signupButton.addEventListener('click', function(event) {  
       console.log('it is clicked');
      event.preventDefault(); 
      window.location.href = '/student_register';
    }) 
    forgotButton.addEventListener('click',function (event) {
      event.preventDefault();
      window.location.href = '/reset-password-page';   
  })}); 
