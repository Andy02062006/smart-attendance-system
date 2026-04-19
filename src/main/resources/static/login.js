document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const role = document.getElementById('role').value;
    const errorMessage = document.getElementById('errorMessage');

    // For demo purposes, we accept any login but store the role
    if (username && password) {
        console.log('Login successful for:', username, 'as', role);
        localStorage.setItem('isAuthenticated', 'true');
        localStorage.setItem('user', username);
        localStorage.setItem('role', role);
        window.location.href = 'index.html';
    } else {
        errorMessage.textContent = 'Please enter both username and password.';
    }
});