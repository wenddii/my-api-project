const API = "http://127.0.0.1:8000/api";

let token = localStorage.getItem("token");

// ----------------------
// LOAD THREADS
// ----------------------
async function loadThreads() {
    try {
        const res = await fetch("http://127.0.0.1:8000/api/threads/");
        const text = await res.text();

        console.log("RAW RESPONSE:", text);  // <-- THIS LINE

        const data = JSON.parse(text);

        const container = document.getElementById("threads");
        container.innerHTML = "";

        data.forEach(t => {
            const div = document.createElement("div");
            div.innerHTML = `
                <h3>${t.title}</h3>
                <p>${t.content}</p>
            `;
            container.appendChild(div);
        });

    } catch (err) {
        console.error("Failed to load threads:", err);
    }
}
// ----------------------
// LOGIN
// ----------------------
document.getElementById("loginForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    try {
        const res = await fetch(`${API}/token/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ username, password })
        });

        const data = await res.json();

        if (data.access) {
            token = data.access;
            localStorage.setItem("token", token);
            console.log("Logged in successfully");
        } else {
            console.error("Login failed:", data);
        }

    } catch (err) {
        console.error("Login error:", err);
    }
});

// ----------------------
// CREATE THREAD
// ----------------------
document.getElementById("threadForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const title = document.getElementById("title").value;
    const content = document.getElementById("content").value;

    if (!token) {
        alert("You must login first");
        return;
    }

    try {
        const res = await fetch(`${API}/threads/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            },
            body: JSON.stringify({ title, content })
        });

        if (!res.ok) {
            throw new Error("Failed to create thread");
        }

        document.getElementById("title").value = "";
        document.getElementById("content").value = "";

        loadThreads();

    } catch (err) {
        console.error("Create thread error:", err);
    }
});

// ----------------------
// INIT
// ----------------------
loadThreads();