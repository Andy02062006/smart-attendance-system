document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorMessage = document.getElementById('errorMessage');

    // Simple login logic: accept any non-empty username/password
    if (username && password) {
        console.log('Login successful for:', username);
        // Save simple flag for "auth" (not secure, but simple as requested)
        localStorage.setItem('isAuthenticated', 'true');
        window.location.href = 'index.html';
    } else {
        errorMessage.textContent = 'Please enter both username and password.';
    }
});