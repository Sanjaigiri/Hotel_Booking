// ===== Contact Form Submission =====
const contactForm = document.getElementById('contactForm');
const responseMessage = document.getElementById('responseMessage');

contactForm.addEventListener('submit', function(e) {
    e.preventDefault();

    // Collect form data (optional, for actual backend submission)
    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const message = document.getElementById('message').value.trim();

    if(name && email && message){
        // Simulate successful submission
        responseMessage.textContent = `Thank you, ${name}! Your message has been sent successfully.`;
        responseMessage.style.color = 'green';
        responseMessage.classList.remove('hidden');

        // Clear form
        contactForm.reset();
    } else {
        responseMessage.textContent = "Please fill all fields!";
        responseMessage.style.color = 'red';
        responseMessage.classList.remove('hidden');
    }
});
