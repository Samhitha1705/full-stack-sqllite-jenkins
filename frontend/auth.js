// Toggle between forms
document.getElementById("show-login").addEventListener("click", () => {
  document.getElementById("register-form").style.display = "none";
  document.getElementById("login-form").style.display = "block";
});

document.getElementById("show-register").addEventListener("click", () => {
  document.getElementById("login-form").style.display = "none";
  document.getElementById("register-form").style.display = "block";
});

// Register user
document.getElementById("register-btn").addEventListener("click", async () => {
  const username = document.getElementById("reg-username").value;
  const password = document.getElementById("reg-password").value;

  const res = await fetch("/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });

  const data = await res.json();
  document.getElementById("register-msg").innerText = data.message;

  if (res.ok) {
    setTimeout(() => {
      document.getElementById("register-form").style.display = "none";
      document.getElementById("login-form").style.display = "block";
    }, 1000);
  }
});

// Login user
document.getElementById("login-btn").addEventListener("click", async () => {
  const username = document.getElementById("login-username").value;
  const password = document.getElementById("login-password").value;

  const res = await fetch("/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });

  const data = await res.json();
  document.getElementById("login-msg").innerText = data.message;

  if (res.ok) {
    window.location.href = "/dashboard";
  }
});
