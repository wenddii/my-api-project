const API = "http://127.0.0.1:8000/api";

const params = new URLSearchParams(window.location.search);
const threadId = params.get("id");

async function loadThread() {
    const res = await fetch(`${API}/threads/${threadId}/`);
    const data = await res.json();

    document.getElementById("thread").innerHTML = `
        <h2>${data.title}</h2>
        <p>${data.content}</p>
    `;
}

async function loadComments() {
    const res = await fetch(`${API}/threads/${threadId}/comments/`);
    const data = await res.json();

    const container = document.getElementById("comments");
    container.innerHTML = "";

    data.forEach(c => {
        const div = document.createElement("div");
        div.innerHTML = `
            <p>${c.content}</p>
            <small>score: ${c.score || 0}</small>
            <hr/>
        `;
        container.appendChild(div);
    });
}

document.getElementById("commentForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const content = document.getElementById("commentContent").value;

    await fetch(`${API}/threads/${threadId}/comments/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ content })
    });

    loadComments();
});

loadThread();
loadComments();