document.addEventListener('DOMContentLoaded', function() {
    // --- Бургер-меню ---
    const burger = document.querySelector('.burger');
    const nav = document.querySelector('.nav');

    if (burger && nav) {
        burger.addEventListener('click', function() {
            const isExpanded = this.getAttribute('aria-expanded') === 'true';
            nav.classList.toggle('active');
            this.setAttribute('aria-expanded', !isExpanded);
        });
    }

    // --- Универсальная функция маски и валидации телефона ---
    function attachPhoneMask(phoneInput, phoneError) {
        if (!phoneInput) return;

        phoneInput.addEventListener('input', function() {
            let value = this.value.replace(/\D/g, '');
            if (value.startsWith('8')) value = '7' + value.slice(1);
            if (value.length > 0 && value[0] === '9') value = '7' + value;
            value = value.slice(0, 11);

            let formatted = '';
            if (value.length > 0) {
                formatted = '+7';
                if (value.length > 1) formatted += ' (' + value.slice(1, 4);
                if (value.length >= 5) formatted += ') ' + value.slice(4, 7);
                if (value.length >= 8) formatted += '-' + value.slice(7, 9);
                if (value.length >= 10) formatted += '-' + value.slice(9, 11);
            }

            this.value = formatted;
            if (phoneError) validatePhone(this.value, phoneInput, phoneError);
        });
    }

    function validatePhone(value, phoneInput, phoneError) {
        if (!phoneInput || !phoneError) return false;
        const digits = value.replace(/\D/g, '');
        const isValid = /^7\d{10}$/.test(digits);

        if (value.trim() === '') {
            phoneError.textContent = '';
            phoneInput.classList.remove('form__input_invalid', 'form__input_valid');
            return false;
        }

        if (isValid) {
            phoneError.textContent = '✓ Номер корректен';
            phoneError.style.color = '#28CB8B';
            phoneInput.classList.remove('form__input_invalid');
            phoneInput.classList.add('form__input_valid');
            return true;
        } else {
            phoneError.textContent = 'Введите корректный номер';
            phoneError.style.color = '#E53935';
            phoneInput.classList.remove('form__input_valid');
            phoneInput.classList.add('form__input_invalid');
            return false;
        }
    }

    // --- Форма обратной связи ---
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        const contactPhone = document.getElementById('id_phone');
        const contactPhoneError = document.getElementById('phoneError');
        if (contactPhone) attachPhoneMask(contactPhone, contactPhoneError);
    }

    // --- Форма регистрации ---
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        const phoneInput = document.getElementById('id_phone');
        const phoneError = document.getElementById('regPhoneError');
        const passwordInput = document.getElementById('id_password1');
        const passwordConfirm = document.getElementById('id_password2');
        const passwordMatchError = document.getElementById('passwordMatchError');

        if (phoneInput) attachPhoneMask(phoneInput, phoneError);

        function checkPasswords() {
            if (!passwordInput || !passwordConfirm) return true;
            if (passwordConfirm.value === '') {
                passwordMatchError.textContent = '';
                passwordConfirm.classList.remove('form__input_invalid', 'form__input_valid');
                return false;
            }
            if (passwordInput.value === passwordConfirm.value) {
                passwordMatchError.textContent = '✓ Пароли совпадают';
                passwordMatchError.style.color = '#28CB8B';
                passwordConfirm.classList.remove('form__input_invalid');
                passwordConfirm.classList.add('form__input_valid');
                return true;
            } else {
                passwordMatchError.textContent = 'Пароли не совпадают';
                passwordMatchError.style.color = '#E53935';
                passwordConfirm.classList.remove('form__input_valid');
                passwordConfirm.classList.add('form__input_invalid');
                return false;
            }
        }

        if (passwordConfirm) passwordConfirm.addEventListener('input', checkPasswords);
        if (passwordInput) passwordInput.addEventListener('input', checkPasswords);
    }

    // ============================================
    // ЛОГИКА СЛАЙДЕРА С ТУРАМИ
    // ============================================
    const track = document.getElementById('tour-slider');
    const prevBtn = document.getElementById('tour-prev');
    const nextBtn = document.getElementById('tour-next');

    if (track && prevBtn && nextBtn) {
        function getScrollAmount() {
            const card = track.querySelector('.tour-card');
            if (!card) return 300;
            // Берем реальную ширину карточки и прибавляем отступ (gap: 30px)
            return card.offsetWidth + 30;
        }

        nextBtn.addEventListener('click', () => {
            track.scrollBy({ left: getScrollAmount(), behavior: 'smooth' });
        });

        prevBtn.addEventListener('click', () => {
            track.scrollBy({ left: -getScrollAmount(), behavior: 'smooth' });
        });
    }
});