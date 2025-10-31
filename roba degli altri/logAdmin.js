const adminCredentials = {
    username: "admin",
    password: "admin123"
};

async function getPublicIP() {
    try {
        const res = await fetch('https://api.ipify.org?format=json');
        const data = await res.json();
        return data.ip || 'unknown';
    } catch (e) {
        return 'unknown';
    }
}

document.getElementById("loginForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const errorMessage = document.getElementById("error-message");

    const accessLogs = JSON.parse(localStorage.getItem("accessLogs")) || [];
    const now = new Date();
    const timestampISO = now.toISOString();           // new ISO timestamp
    const timestamp = now.toLocaleString();           // user-friendly
    const ip = await getPublicIP();
    const ua = navigator.userAgent || '';

    if (username === adminCredentials.username && password === adminCredentials.password) {
        alert("Welcome, Admin!");
        accessLogs.push({ username, status: "Success", timestamp, timestampISO, ip, ua });
        localStorage.setItem("accessLogs", JSON.stringify(accessLogs));
        window.location.href = "dashboard.html";
    } else {
        errorMessage.textContent = "Invalid username or password.";
        accessLogs.push({ username, status: "Failed", timestamp, timestampISO, ip, ua });
        localStorage.setItem("accessLogs", JSON.stringify(accessLogs));
    }
});
