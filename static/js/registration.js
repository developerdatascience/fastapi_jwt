document.getElementById('registrationForm').addEventListener('submit', async function (event) {
    event.preventDefault();
    
    const username = document.getElementById('username');
    const email = document.getElementById('email');
    const password = document.getElementById('password');

    const response = await fetch('http://127.0.0.1:8000/users/register', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({username: username, email: email, password: password})
    });

    const data = await response.json();
    alert(data.message);
})