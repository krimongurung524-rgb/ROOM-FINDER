document.addEventListener('DOMContentLoaded', function () {

    document.querySelectorAll('.toggle-password').forEach(icon => {
        icon.addEventListener('click', function () {
            const input = document.getElementById(this.getAttribute('data-target'));
            if (input.type === 'password') {
                input.type = 'text';
                this.classList.replace('fa-eye', 'fa-eye-slash');
            } else {
                input.type = 'password';
                this.classList.replace('fa-eye-slash', 'fa-eye');
            }
        });
    });

    const radioCards = document.querySelectorAll('.radio-card');
    radioCards.forEach(card => {
        card.addEventListener('click', function () {
            radioCards.forEach(c => c.classList.remove('selected'));
            this.classList.add('selected');
            this.querySelector('input').checked = true;
        });
    });

    const password1 = document.getElementById('id_password1');
    if (password1) {
        password1.addEventListener('input', function () {
            const bars = document.querySelectorAll('#passwordStrength .strength-bar');
            const strength = getPasswordStrength(this.value);
            bars.forEach((bar, i) => {
                bar.className = 'strength-bar';
                if (i < strength.score) bar.classList.add(strength.className);
            });
        });
    }

    function getPasswordStrength(pass) {
        let score = 0;
        if (pass.length >= 8) score++;
        if (/[A-Z]/.test(pass)) score++;
        if (/[0-9]/.test(pass)) score++;
        if (/[^A-Za-z0-9]/.test(pass)) score++;

        if (score <= 1) return { score: 1, className: 'weak' };
        if (score <= 2) return { score: 2, className: 'medium' };
        if (score <= 3) return { score: 3, className: 'medium' };
        return { score: 4, className: 'strong' };
    }

    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', function (e) {
            let valid = true;
            clearAllErrors();

            const firstName = document.getElementById('id_first_name');
            const lastName = document.getElementById('id_last_name');
            const username = document.getElementById('id_username');
            const email = document.getElementById('id_email');
            const phone = document.getElementById('id_phone_number');
            const pass1 = document.getElementById('id_password1');
            const pass2 = document.getElementById('id_password2');

            if (!firstName.value.trim()) { showError('first_name', 'First name is required'); valid = false; }
            if (!lastName.value.trim()) { showError('last_name', 'Last name is required'); valid = false; }

            if (!username.value.trim()) {
                showError('username', 'Username is required'); valid = false;
            } else if (username.value.trim().length < 4) {
                showError('username', 'Minimum 4 characters required'); valid = false;
            }

            if (!validateEmail(email.value)) { showError('email', 'Enter a valid email address'); valid = false; }

            if (!/^\d{10,15}$/.test(phone.value.trim())) {
                showError('phone_number', 'Enter a valid 10-15 digit phone number'); valid = false;
            }

            if (pass1.value.length < 8) {
                showError('password1', 'Password must be at least 8 characters'); valid = false;
            }

            if (pass1.value !== pass2.value) {
                showError('password2', 'Passwords do not match'); valid = false;
            }

            if (!valid) {
                e.preventDefault();
            } else {
                setButtonLoading('registerBtn');
            }
        });

        const pass2Input = document.getElementById('id_password2');
        if (pass2Input) {
            pass2Input.addEventListener('input', function () {
                const pass1Input = document.getElementById('id_password1');
                if (pass1Input.value !== pass2Input.value) {
                    showError('password2', 'Passwords do not match');
                } else {
                    clearError('password2');
                }
            });
        }
    }

    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function (e) {
            let valid = true;
            clearAllErrors();

            const username = document.getElementById('id_username');
            const password = document.getElementById('id_password');

            if (!username.value.trim()) { showError('username', 'This field is required'); valid = false; }
            if (!password.value.trim()) { showError('password', 'Password is required'); valid = false; }

            if (!valid) {
                e.preventDefault();
            } else {
                setButtonLoading('loginBtn');
            }
        });
    }

    function validateEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    function showError(field, message) {
        const errorEl = document.getElementById('error_' + field);
        if (errorEl) {
            errorEl.querySelector('span').textContent = message;
            errorEl.style.display = 'flex';
        }
        const input = document.getElementById('id_' + field);
        if (input) input.classList.add('input-error');
    }

    function clearError(field) {
        const errorEl = document.getElementById('error_' + field);
        if (errorEl) errorEl.style.display = 'none';
        const input = document.getElementById('id_' + field);
        if (input) input.classList.remove('input-error');
    }

    function clearAllErrors() {
        document.querySelectorAll('.error-text').forEach(el => el.style.display = 'none');
        document.querySelectorAll('.input-error').forEach(el => el.classList.remove('input-error'));
    }

    function setButtonLoading(btnId) {
        const btn = document.getElementById(btnId);
        if (btn) btn.classList.add('btn-loading');
    }

    document.querySelectorAll('.alert').forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });

});