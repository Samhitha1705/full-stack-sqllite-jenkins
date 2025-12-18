function login() {
    const username = document.getElementById("username").value.trim();
    if (!username) {
        alert("Please enter a username");
        return;
    }

    fetch("/api/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({username})
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("response").innerText = data.message || data.error;
        loadHistory();
    })
    .catch(err => {
        document.getElementById("response").innerText = "Error connecting to backend";
    });
}

function loadHistory() {
    fetch("/api/logins")
    .then(res => res.json())
    .then(data => {
        const ul = document.getElementById("history");
        ul.innerHTML = "";
        data.forEach(item => {
            const li = document.createElement("li");
            li.textContent = `${item.username} → ${item.time}`;
            ul.appendChild(li);
        });
    });
}

// Load history on page load
window.onload = loadHistory;
