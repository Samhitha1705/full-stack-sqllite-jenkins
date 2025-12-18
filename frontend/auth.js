function register() {
    const username = document.getElementById("regUser").value.trim();
    const password = document.getElementById("regPwd").value.trim();
    if (!username || !password) {
        alert("Enter username and password");
        return;
    }

    fetch("/api/register", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({username, password})
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("regMsg").innerText = data.message || data.error;
    });
}

function login() {
    const username = document.getElementById("loginUser").value.trim();
    const password = document.getElementById("loginPwd").value.trim();
    if (!username || !password) {
        alert("Enter username and password");
        return;
    }

    fetch("/api/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({username, password})
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("loginMsg").innerText = data.message || data.error;
        if (data.message) {
            window.location.href = "/dashboard";
        }
    });
}
