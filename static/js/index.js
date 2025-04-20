document.addEventListener('DOMContentLoaded', function () {
  // Handle button clicks
  function handleButtonClick(event) {
    const url = event.target.getAttribute('url');
    if (url) {
      window.location.href = url;
    }
  }

  const studentBtn = document.getElementById('student-login-btn');
  const recruiterBtn = document.getElementById('recruiter-login-btn');
  const startCareerBtn = document.getElementById('start-career-btn');

  if (studentBtn) studentBtn.addEventListener('click', handleButtonClick);
  if (recruiterBtn) recruiterBtn.addEventListener('click', handleButtonClick);
  if (startCareerBtn) startCareerBtn.addEventListener('click', handleButtonClick);

  // Scroll animation for stats
  const stats = document.querySelectorAll('.stat-item');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate');
      }
    });
  }, {
    threshold: 0.5
  });

  stats.forEach(stat => observer.observe(stat));

  // Auto-hide flash messages
  const flash = document.querySelector('.flash-message');
  if (flash) {
    setTimeout(() => {
      flash.style.display = 'none';
    }, 3000);
  }
});
