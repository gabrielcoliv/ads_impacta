const API_URL = "http://127.0.0.1:5000";

async function fetchAPI(endpoint, method = "GET", body = null) {
    const options = { 
        method,
        headers: { "Content-Type": "application/json" }
    };
    if (body) options.body = JSON.stringify(body);

    const response = await fetch(`${API_URL}${endpoint}`, options);
    return response.json();
}
