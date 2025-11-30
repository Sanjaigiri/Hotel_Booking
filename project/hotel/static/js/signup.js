// ===== PASSWORD TOGGLE =====
document.querySelectorAll('.toggle-password').forEach((toggle, index) => {
  toggle.addEventListener('click', () => {
    const input = document.querySelectorAll('input[type="password"]')[index];
    if (input.type === "password") {
      input.type = "text";
      toggle.textContent = "🙈";
    } else {
      input.type = "password";
      toggle.textContent = "👁️";
    }
  });
});

// ===== FORM VALIDATION =====
document.getElementById("signupForm").addEventListener("submit", function(e) {
  const name = document.getElementById("name").value.trim();
  const email = document.getElementById("email").value.trim();
  const phone = document.getElementById("phone") ? document.getElementById("phone").value.trim() : '';
  const password = document.getElementById("password").value.trim();
  const confirmPassword = document.getElementById("confirmPassword").value.trim();
  const messageBox = document.getElementById("messageBox");

  if (!name || !email || !password || !confirmPassword) {
    e.preventDefault();
    messageBox.style.color = "red";
    messageBox.textContent = "⚠️ Please fill all fields.";
    return;
  }

  // Allow phone in multiple formats: 10 digits or optional + and country code
  if (phone && !/^\+?\d{10,15}$/.test(phone)) {
    e.preventDefault();
    messageBox.style.color = "red";
    messageBox.textContent = "⚠️ Enter a valid phone number (10-15 digits, optional leading +) or leave empty.";
    return;
  }

  if (password.length < 6) {
    e.preventDefault();
    messageBox.style.color = "red";
    messageBox.textContent = "⚠️ Password must be at least 6 characters.";
    return;
  }

  if (password !== confirmPassword) {
    e.preventDefault();
    messageBox.style.color = "red";
    messageBox.textContent = "⚠️ Passwords do not match.";
    return;
  }

  // If validation passes, allow form submission
  messageBox.style.color = "blue";
  messageBox.textContent = "⏳ Creating account...";
});
