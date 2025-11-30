document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("bookForm");
  const totalPriceEl = document.getElementById("totalPrice");

  const checkInInput = document.getElementById("checkIn");
  const checkOutInput = document.getElementById("checkOut");
  const roomTypeSelect = document.getElementById("roomType");
  const guestsInput = document.getElementById("guests");
  const messageBox = document.getElementById("messageBox");

  const phoneInput = document.getElementById("phone");
  const otpInput = document.getElementById("otp");
  const sendOtpBtn = document.getElementById("sendOtpBtn");
  const otpMessage = document.getElementById("otpMessage");

  // ===== OTP VARIABLES =====
  let otpSent = false;
  let otpVerified = false;
  let otpCooldown = false;

  // ===== PREFILL FROM SESSION (after login redirect) =====
  try {
    const stored = sessionStorage.getItem('bookingData');
    if (stored) {
      const bd = JSON.parse(stored);
      if (bd.name) document.getElementById('name').value = bd.name;
      if (bd.email) document.getElementById('email').value = bd.email;
      if (bd.phone) document.getElementById('phone').value = bd.phone;
      if (bd.roomType) document.getElementById('roomType').value = bd.roomType;
      if (bd.checkIn) document.getElementById('checkIn').value = bd.checkIn;
      if (bd.checkOut) document.getElementById('checkOut').value = bd.checkOut;
      if (bd.guests) document.getElementById('guests').value = bd.guests;
      // recalc price
      calculatePrice();
      sessionStorage.removeItem('bookingData');
    }
  } catch (e) { /* No prefill data */ }

  // ===== GET CSRF TOKEN =====
  function getCsrfToken() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
    return csrfToken ? csrfToken.value : '';
  }

  // ===== OTP REQUEST (SEND OTP) =====
  sendOtpBtn.addEventListener("click", async () => {
    // If booking requires login, save current form to sessionStorage and redirect to login
    if (window.REQUIRES_LOGIN) {
      const save = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        phone: document.getElementById('phone').value,
        roomType: document.getElementById('roomType').value,
        checkIn: document.getElementById('checkIn').value,
        checkOut: document.getElementById('checkOut').value,
        guests: document.getElementById('guests').value
      };
      sessionStorage.setItem('bookingData', JSON.stringify(save));
      // redirect to login and pass next param to return here
      window.location.href = '/login/?next=/booking/';
      return;
    }
    const phone = phoneInput.value.trim();

    // Validate phone
    if (!phoneInput.checkValidity()) {
      alert("Please enter a valid 10-digit phone number first!");
      return;
    }

    if (otpCooldown) {
      alert("You can request OTP again after 60 seconds.");
      return;
    }

    // Disable button and show loading
    sendOtpBtn.disabled = true;
    sendOtpBtn.textContent = "Sending...";
    otpMessage.textContent = "Sending OTP...";
    otpMessage.style.color = "blue";

    try {
      // Send OTP request to backend
      const response = await fetch('/booking/request-otp/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify({ phone: phone })
      });

      const data = await response.json();

      if (data.ok) {
        otpSent = true;
        // If backend indicates mock/dev mode, show the dev message and (optionally) highlight the code
        if (data.mock) {
          otpMessage.textContent = data.message || `OTP sent successfully! [DEV MODE: Use ${data.mock_code || '123456'}]`;
          otpMessage.style.color = "green";
        } else {
          otpMessage.textContent = data.message || "OTP sent successfully! Check your phone.";
          otpMessage.style.color = "green";
        }

        // Start cooldown to prevent spamming
        otpCooldown = true;
        let countdown = 60;
        const cooldownInterval = setInterval(() => {
          countdown--;
          sendOtpBtn.textContent = `Resend (${countdown}s)`;
          if (countdown <= 0) {
            clearInterval(cooldownInterval);
            otpCooldown = false;
            sendOtpBtn.disabled = false;
            sendOtpBtn.textContent = "Send OTP";
          }
        }, 1000);
      } else {
        otpMessage.textContent = data.message || "Failed to send OTP. Please try again.";
        otpMessage.style.color = "red";
        sendOtpBtn.disabled = false;
        sendOtpBtn.textContent = "Send OTP";
      }
    } catch (error) {
      console.error("Error sending OTP:", error);
      otpMessage.textContent = "Network error. Please check your connection.";
      otpMessage.style.color = "red";
      sendOtpBtn.disabled = false;
      sendOtpBtn.textContent = "Send OTP";
    }
  });

  // ===== ROOM PRICES & CALCULATION =====
  const roomPrices = {
    single: 1200,
    deluxe: 4500,
    suite: 6000,
    luxury: 8500,
    dorm: 1200,
    ocean: 9000,
    executive: 6500,
    luxury_villa: 12000,
  };

  const calculatePrice = () => {
    const roomType = roomTypeSelect.value;
    const guests = parseInt(guestsInput.value) || 0;
    const checkIn = new Date(checkInInput.value);
    const checkOut = new Date(checkOutInput.value);

    if (roomType && checkIn && checkOut && checkOut > checkIn && guests > 0) {
      const days = Math.ceil((checkOut - checkIn) / (1000 * 60 * 60 * 24));
      const perNight = roomPrices[roomType] || 0;
      const total = days * perNight * guests;
      totalPriceEl.textContent = `₹${total.toLocaleString("en-IN")}`;
    } else {
      totalPriceEl.textContent = "₹0";
    }
  };

  [roomTypeSelect, checkInInput, checkOutInput, guestsInput].forEach(el =>
    el.addEventListener("change", calculatePrice)
  );

  // ===== FORM SUBMISSION & OTP VALIDATION =====
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // ===== OTP VALIDATION =====
    if (!otpSent) {
      showMessage("⚠️ Please request OTP first by clicking 'Send OTP'.", "error");
      return;
    }

    const phone = phoneInput.value.trim();
    const otp = otpInput.value.trim();

    if (!otp || otp.length !== 6) {
      showMessage("⚠️ Please enter a valid 6-digit OTP.", "error");
      return;
    }

    // Other validations
    if (!roomTypeSelect.value) {
      showMessage("⚠️ Please select a room type.", "error");
      return;
    }
    if (!checkInInput.value || !checkOutInput.value || new Date(checkOutInput.value) <= new Date(checkInInput.value)) {
      showMessage("⚠️ Please enter valid check-in and check-out dates.", "error");
      return;
    }
    if (guestsInput.value < 1) {
      showMessage("⚠️ Please enter the number of guests.", "error");
      return;
    }

    // Verify OTP with backend
    showMessage("🔄 Verifying OTP...", "info");

    try {
      const response = await fetch('/booking/verify-otp/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify({ phone: phone, otp: otp })
      });

      const data = await response.json();

      if (data.ok) {
        showMessage("✅ OTP verified! Redirecting to payment...", "success");
        // Submit booking to server to store in database
        const bookingData = {
          name: document.getElementById('name').value,
          email: document.getElementById('email').value,
          phone: phone,
          roomType: roomTypeSelect.value,
          checkIn: checkInInput.value,
          checkOut: checkOutInput.value,
          guests: guestsInput.value,
          totalPrice: totalPriceEl.textContent
        };

        try {
          const saveResp = await fetch('/booking/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
              'X-CSRFToken': getCsrfToken()
            },
            body: new URLSearchParams(bookingData)
          });

          const saveJson = await saveResp.json();
          if (saveJson.ok) {
            showMessage('✅ Booking saved. Redirecting to payment...', 'success');
            setTimeout(() => { window.location.href = saveJson.redirect || '/booking/payment/'; }, 800);
          } else {
            showMessage('❌ ' + (saveJson.message || 'Failed to save booking.'), 'error');
          }
        } catch (err) {
          console.error('Error saving booking:', err);
          showMessage('❌ Network error while saving booking.', 'error');
        }
      } else {
        showMessage(`❌ ${data.message || 'Invalid OTP. Please try again.'}`, "error");
      }
    } catch (error) {
      console.error("Error verifying OTP:", error);
      showMessage("❌ Network error. Please check your connection.", "error");
    }
  });

  // ===== SHOW MESSAGE =====
  function showMessage(msg, type) {
    messageBox.textContent = msg;
    if (type === "error") {
      messageBox.style.color = "red";
    } else if (type === "success") {
      messageBox.style.color = "green";
    } else if (type === "info") {
      messageBox.style.color = "blue";
    }
    messageBox.style.fontWeight = "600";
    messageBox.style.textAlign = "center";
    messageBox.style.marginTop = "10px";
  }
});
