document.getElementById("forgotForm").addEventListener("submit", function (e) {
    let email = document.getElementById("email").value;

    if (email.trim() === "") {
        alert("Please enter your email!");
        e.preventDefault();
        return;
    }

    // Simple loading effect
    let btn = document.querySelector("button");
    btn.innerText = "Sending...";
    btn.style.opacity = "0.7";
});
