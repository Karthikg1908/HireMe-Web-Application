document.addEventListener('DOMContentLoaded', function () {
    function handleButtonClick(event) {
        const url = event.target.getAttribute('data-url');
        if (url) {
            window.location.href = url;
        }
    }

    const studentLoginBtn = document.getElementById('student-login-btn');
    const recruiterLoginBtn = document.getElementById('recruiter-login-btn');
    const startCareerBtn = document.getElementById('start-career-btn');

    if (studentLoginBtn) studentLoginBtn.addEventListener('click', handleButtonClick);
    if (recruiterLoginBtn) recruiterLoginBtn.addEventListener('click', handleButtonClick);
    if (startCareerBtn) startCareerBtn.addEventListener('click', handleButtonClick);

    const roleSelectButton = document.getElementById('roleSelectButton');
    const roleModal = document.getElementById('roleModal');
    const chatPanel = document.getElementById('chatPanel');
    const chatContent = document.getElementById('chatContent');
    const chatOptions = document.querySelector('.chat-options');
    
    roleSelectButton.addEventListener('click', () => {
        roleModal.style.display = 'block';
    });

    document.getElementById('jobSeekerBtn').addEventListener('click', () => {
        sessionStorage.setItem('role', 'jobSeeker');
        roleModal.style.display = 'none';
        showChat();
    });

    document.getElementById('recruiterBtn').addEventListener('click', () => {
        sessionStorage.setItem('role', 'recruiter');
        roleModal.style.display = 'none';
        showChat();
    });

    function showChat() {
        const role = sessionStorage.getItem('role');
        let questionsAndAnswers;
        let buttonsHTML = '';

        if (role === 'jobSeeker') {
            questionsAndAnswers = [
                { question: "How do I apply for a job?", answer: "Click the 'Apply' button next to the job you're interested in." },
        { question: "Can I apply for more than one job?", answer: "Yes, you can apply for multiple jobs as long as they are open." },
        { question: "How do I update my profile?", answer: "Go to your profile page and click 'Edit Profile' to make changes." },
        { question: "How do I know if my application was successful?", answer: "The button will change to 'Applied' once you've submitted your application." },
        { question: "Is there a way to contact the recruiter directly?", answer: "Some job posts include a contact option—check the job details for recruiter info." },
        { question: "What should I do if I forget my password?", answer: "You can reset your password using the 'Forgot Password' link." },
        { question: "Can I edit my application after submitting?", answer: "You can’t edit once submitted, but you can withdraw and reapply if needed." },
        { question: "What happens after I apply for a job?", answer: "Your application is sent to the recruiter, who may review and contact you." }
    ];
} else if (role === 'recruiter') {
    questionsAndAnswers = [
        { question: "How do I add a new job?", answer: "Log in as recruiter, go to the 'Create Job' section, and fill in the details." },
        { question: "Where can I view student applications?", answer: "Go to the 'Reports' section to see who applied." },
        { question: "How do I download the job report?", answer: "Click the 'Download Report' button on the report page." },
        { question: "How do I mark a job as 'Closed'?", answer: "In the 'Manage Jobs' section, select the job and change its status to 'Closed'." },
        { question: "Can I edit a job after posting it?", answer: "Yes, go to 'Manage Jobs', select the job, and click 'Edit' to update the details." },
        { question: "Can I re-open a closed job?", answer: "Yes, just change the status back to 'Open' in the 'Manage Jobs' section." }
    ];
        }

        chatContent.innerHTML = '';
        questionsAndAnswers.forEach(item => {
            buttonsHTML += `<button class="question-btn" data-answer="${item.answer}">${item.question}</button>`;
        });

        chatOptions.innerHTML = buttonsHTML;
        chatPanel.style.display = 'block';

        const questionButtons = document.querySelectorAll('.question-btn');
        questionButtons.forEach(button => {
            button.addEventListener('click', function() {
                userQuery(button.innerText, button.getAttribute('data-answer'));
            });
        });
    }

   function userQuery(question, answer) {
    const chatBody = document.getElementById('chatContent');

    // Create and append user's message
    const userMsg = document.createElement('div');
    userMsg.className = 'chat-message user';
    userMsg.innerText = question;
    chatBody.appendChild(userMsg);

    // Create typing indicator with bouncing dots
    const typingMsg = document.createElement('div');
    typingMsg.className = 'chat-message bot typing';
    typingMsg.innerHTML = `
        <span class="typing-dots">
            <span></span><span></span><span></span>
        </span>
    `;
    
    // Insert typing directly after user message
    chatBody.insertBefore(typingMsg, userMsg.nextSibling);
    chatBody.scrollTop = chatBody.scrollHeight;

    setTimeout(() => {
        typingMsg.remove();

        const botMsg = document.createElement('div');
        botMsg.className = 'chat-message bot';
        botMsg.innerText = answer;

        // Insert the actual answer after the user message
        chatBody.insertBefore(botMsg, userMsg.nextSibling);
        chatBody.scrollTop = chatBody.scrollHeight;
    }, 1200);
}



});



document.addEventListener('DOMContentLoaded', () => {
  const track = document.querySelector('.companies-track');
  const logos = document.querySelectorAll('.company-logo');
  const visibleCount = 4;
  const total = logos.length;
  let currentIndex = 0;

  function slideLogos() {
    currentIndex++;
    if (currentIndex > total - visibleCount) {
      currentIndex = 0;
    }
    const shift = -(100 / visibleCount) * currentIndex;
    track.style.transform = `translateX(${shift}%)`;
  }

  // Auto-scroll
  let autoScroll = setInterval(slideLogos, 4000);

  // Manual scroll on click
  document.querySelector('.companies-wrapper').addEventListener('click', () => {
    clearInterval(autoScroll); // Optional: pause auto scroll
    slideLogos();
  });
});

function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

window.onscroll = function() {
    const btn = document.getElementById("scrollToTopBtn");
    if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
        btn.style.display = "block";
    } else {
        btn.style.display = "none";
    }
};


  const counters = document.querySelectorAll('.stat-number');
  const speed = 100;

  const animateCount = (counter) => {
    const target = +counter.getAttribute('data-target');
    let current = 0;

    const update = () => {
      const increment = Math.ceil(target / speed);
      if (current < target) {
        current += increment;
        counter.innerText = current;
        setTimeout(update, 20);
      } else {
        counter.innerText = `${target}+`;
      }
    };
    update();
  };

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        counters.forEach(counter => animateCount(counter));
        observer.disconnect();
      }
    });
  }, { threshold: 0.5 });

  observer.observe(document.querySelector('.stats'));

