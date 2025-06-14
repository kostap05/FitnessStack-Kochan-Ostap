document.addEventListener("DOMContentLoaded", () => {
  const registerForm = document.getElementById("registerForm");

  registerForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("username", document.getElementById("username").value.trim());
    formData.append("email", document.getElementById("email").value.trim());
    formData.append("password", document.getElementById("password").value.trim());

    const weight = parseFloat(document.getElementById("weight").value);
    if (!isNaN(weight)) formData.append("weight", weight);

    const height = parseFloat(document.getElementById("height").value);
    if (!isNaN(height)) formData.append("height", height);

    const goal = document.getElementById("goal").value.trim();
    if (goal) formData.append("goal", goal);

    const avatarInput = document.getElementById("avatar");
    if (avatarInput.files.length > 0) {
      formData.append("avatar", avatarInput.files[0]);
    }

    try {
      const response = await fetch("http://127.0.0.1:8000/auth/register", { // <-- исправлено
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const error = await response.json();
        alert("Error: " + (error.detail || "Unknown error"));
      } else {
        alert("Registration successful! You can now log in.");
        window.location.href = "login.html";
      }
    } catch (err) {
      console.error(err);
      alert("Registration failed. Check console for details.");
    }
  });
});


document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("loginForm");

  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const formData = new FormData();
      formData.append("username", document.getElementById("username").value.trim());
      formData.append("password", document.getElementById("password").value.trim());

      try {
        const response = await fetch("http://127.0.0.1:8000/auth/login", {
          method: "POST",
          body: formData,
        });

        if (!response.ok) {
          const error = await response.json();
          alert("Error: " + (error.detail || "Invalid credentials"));
        } else {
          const data = await response.json();
          localStorage.setItem("access_token", data.access_token);
          alert("Login successful! 🎉");
          window.location.href = "index";
        }
      } catch (err) {
        console.error(err);
        alert("Login failed. Check console for details.");
      }
    });
  }
});
