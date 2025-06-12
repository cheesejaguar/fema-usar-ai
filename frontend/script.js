const API_KEY = 'your-api-key'; // replace with your API key
const BASE_URL = '';

async function chat() {
    const message = document.getElementById('message').value;
    const res = await fetch(`${BASE_URL}/api/chat`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-API-Key': API_KEY
        },
        body: JSON.stringify({ message })
    });
    const data = await res.json();
    document.getElementById('chatResponse').textContent = data.response || data.error;
}

document.getElementById('sendBtn').addEventListener('click', chat);

async function generateICS() {
    const incident = document.getElementById('incident').value;
    const res = await fetch(`${BASE_URL}/api/ics205`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-API-Key': API_KEY
        },
        body: JSON.stringify({ incident })
    });
    const data = await res.json();
    document.getElementById('icsResponse').textContent = data.ics205 || data.error;
}

document.getElementById('icsBtn').addEventListener('click', generateICS);
