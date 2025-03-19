// authentication/static/js/script.js

document.addEventListener('DOMContentLoaded', () => {
    // Sign In Form
    const signinForm = document.getElementById('signin-form');
    if (signinForm) {
        signinForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            try {
                const response = await fetch('/signin/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken,
                    },
                    body: JSON.stringify({ username, password }),
                });

                const data = await response.json();
                const errorMessage = document.getElementById('error-message');
                errorMessage.textContent = '';

                if (data.status === 'success') {
                    window.location.href = data.redirect; // Redirect to /verify/ or /
                } else {
                    errorMessage.textContent = data.message;
                }
            } catch (error) {
                document.getElementById('error-message').textContent = 'An error occurred. Please try again.';
            }
        });
    }

    // Sign Up Form
    const signupForm = document.getElementById('signup-form');
    if (signupForm) {
        signupForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const password_confirm = document.getElementById('password_confirm').value;
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            try {
                const response = await fetch('/signup/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken,
                    },
                    body: JSON.stringify({ username, email, password, password_confirm }),
                });

                const data = await response.json();
                const errorMessage = document.getElementById('error-message');
                const successMessage = document.getElementById('success-message');
                errorMessage.textContent = '';
                successMessage.textContent = '';

                if (data.status === 'success') {
                    successMessage.textContent = data.message;
                } else {
                    errorMessage.textContent = data.message;
                }
            } catch (error) {
                document.getElementById('error-message').textContent = 'An error occurred. Please try again.';
            }
        });
    }
});