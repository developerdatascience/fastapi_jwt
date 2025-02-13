document.getElementById('registrationForm').addEventListener('submit', async (e) => {
    e.preventDefault(); // Prevent default form submission
    
    const messageElement = document.getElementById('message');
    // messageElement.textContent = '';
    // messageElement.className = 'message';

    const formData = {
        username: document.getElementById('username').value,
        email: document.getElementById('email').value,
        password: document.getElementById('password').value
    };

    messageElement.classList.add('active');

    try {
        const response = await fetch('/newaccount', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams(formData)
        });

        const data = await response.json();
        messageElement.textContent = data.message
        message.className = data.status
        messageElement.style.display = 'block'
        // Optional: Clear form or redirect
        document.getElementById('registrationForm').reset();
        setTimeout(() => {
            messageElement.style.display = 'none';
        }, 3000);
        
    } catch (error) {
        messageElement.textContent = error.message;
        messageElement.className = 'message error';
    }
});
