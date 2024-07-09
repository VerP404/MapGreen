// modal.js
document.addEventListener('DOMContentLoaded', function () {
    // Переменные для модального окна входа
    const loginModal = document.getElementById('loginModal');
    const openLoginModalBtn = document.getElementById('openLoginModal');
    const closeLoginModalBtn = loginModal.querySelector('.close');
    const loginForm = document.getElementById('loginForm');
    const loginError = document.getElementById('loginError');
    const loginSuccess = document.getElementById('loginSuccess'); // Добавим элемент для успешного входа

    // Открытие модального окна входа
    if (openLoginModalBtn) {
        openLoginModalBtn.addEventListener('click', function () {
            console.log('Открытие формы входа');
            loginModal.style.display = 'block';
        });
    }

    // Закрытие модального окна входа
    if (closeLoginModalBtn) {
        closeLoginModalBtn.addEventListener('click', function () {
            console.log('Закрытие формы входа');
            loginModal.style.display = 'none';
            loginError.style.display = 'none';  // Скрыть сообщение об ошибке при закрытии
            loginError.textContent = '';  // Очистить сообщение об ошибке
            if (loginSuccess) {
                loginSuccess.style.display = 'none';  // Скрыть сообщение об успехе при закрытии
                loginSuccess.textContent = '';  // Очистить сообщение об успехе
            }
        });
    }

    // Закрытие модального окна входа при нажатии вне его
    window.addEventListener('click', function (event) {
        if (event.target == loginModal) {
            console.log('Закрытие формы входа при нажатии вне окна');
            loginModal.style.display = 'none';
            loginError.style.display = 'none';  // Скрыть сообщение об ошибке при закрытии
            loginError.textContent = '';  // Очистить сообщение об ошибке
            if (loginSuccess) {
                loginSuccess.style.display = 'none';  // Скрыть сообщение об успехе при закрытии
                loginSuccess.textContent = '';  // Очистить сообщение об успехе
            }
        }
    });

    // Обработка формы входа
    if (loginForm) {
        loginForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const formData = new FormData(loginForm);
            const csrfToken = formData.get('csrfmiddlewaretoken');

            var xhr = new XMLHttpRequest();
            xhr.open('POST', loginForm.action, true);
            xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
            xhr.setRequestHeader('X-CSRFToken', csrfToken);
            xhr.onload = function () {
                console.log('XHR onload:', xhr.status, xhr.responseText);
                if (xhr.status === 200) {
                    try {
                        var response = JSON.parse(xhr.responseText);
                        console.log('Response:', response);
                        if (response.success) {
                            console.log('Успешный вход');
                            if (loginSuccess) {
                                loginSuccess.style.display = 'block';
                                loginSuccess.innerHTML = 'Вы успешно вошли в систему. Переадресация...';
                            }
                            setTimeout(() => {
                                console.log('Переадресация на:', response.redirect_url);
                                window.location.href = response.redirect_url || '/'; // Убедитесь, что redirect_url существует
                            }, 2000);  // Переадресация через 2 секунды
                        } else {
                            console.log('Ошибка при входе:', response.errors);
                            loginError.style.display = 'block';  // Показать сообщение об ошибке
                            if (response.errors && typeof response.errors === 'string') {
                                // Если ошибки приходят в виде строки JSON
                                const errors = JSON.parse(response.errors);
                                loginError.innerHTML = Object.values(errors).flat().map(e => e.message || e).join('<br>');
                            } else if (response.errors && typeof response.errors === 'object') {
                                // Если ошибки приходят в виде объекта
                                loginError.innerHTML = Object.values(response.errors).flat().map(e => e.message || e).join('<br>');
                            } else {
                                loginError.innerHTML = 'Вы успешно вошли в систему.';
                                window.location.href = response.redirect_url || '/';
                            }
                        }
                    } catch (e) {
                        console.error('Ошибка обработки ответа:', e);
                        loginError.style.display = 'block';
                        loginError.innerHTML = 'Произошла ошибка при обработке ответа сервера.';
                    }
                } else {
                    console.error('Ошибка сервера:', xhr.status);
                    loginError.style.display = 'block';
                    loginError.innerHTML = 'Ошибка входа. Проверьте учетные данные и повторите попытку';
                }
            };
            xhr.onerror = function () {
                console.error('Ошибка сети');
                loginError.style.display = 'block';
                loginError.innerHTML = 'Ошибка сети. Пожалуйста, попробуйте позже.';
            };
            xhr.send(formData);
        });
    }

    // Переменные для модального окна регистрации
    const signupModal = document.getElementById('signupModal');
    const openSignupModalBtn = document.getElementById('openSignupModal');
    const closeSignupModalBtn = signupModal.querySelector('.close');
    const signupForm = document.getElementById('signupForm');
    const signupError = document.getElementById('signupError');
    const signupSuccess = document.getElementById('signupSuccess');

    // Открытие модального окна регистрации
    if (openSignupModalBtn) {
        openSignupModalBtn.addEventListener('click', function () {
            console.log('Открытие формы регистрации');
            signupModal.style.display = 'block';
        });
    }

    // Закрытие модального окна регистрации
    if (closeSignupModalBtn) {
        closeSignupModalBtn.addEventListener('click', function () {
            console.log('Закрытие формы регистрации');
            signupModal.style.display = 'none';
            signupError.style.display = 'none';  // Скрыть сообщение об ошибке при закрытии
            signupError.textContent = '';  // Очистить сообщение об ошибке
            signupSuccess.style.display = 'none';  // Скрыть сообщение об успехе при закрытии
            signupSuccess.textContent = '';  // Очистить сообщение об успехе
        });
    }

    // Закрытие модального окна регистрации при нажатии вне его
    window.addEventListener('click', function (event) {
        if (event.target == signupModal) {
            console.log('Закрытие формы регистрации при нажатии вне окна');
            signupModal.style.display = 'none';
            signupError.style.display = 'none';  // Скрыть сообщение об ошибке при закрытии
            signupError.textContent = '';  // Очистить сообщение об ошибке
            signupSuccess.style.display = 'none';  // Скрыть сообщение об успехе при закрытии
            signupSuccess.textContent = '';  // Очистить сообщение об успехе
        }
    });

    // Обработка формы регистрации
    if (signupForm) {
        signupForm.addEventListener('submit', function (e) {
            e.preventDefault();
            var formData = new FormData(signupForm);
            var csrfToken = formData.get('csrfmiddlewaretoken');

            var xhr = new XMLHttpRequest();
            xhr.open('POST', signupForm.action, true);
            xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
            xhr.setRequestHeader('X-CSRFToken', csrfToken);
            xhr.onload = function () {
                if (xhr.status === 200) {
                    try {
                        var response = JSON.parse(xhr.responseText);
                        if (response.success) {
                            console.log('Успешная регистрация');
                            signupSuccess.style.display = 'block';
                            signupSuccess.innerHTML = `Вы успешно зарегистрированы как ${response.email}. Переадресация...`;
                            setTimeout(() => {
                                window.location.href = '/';
                            }, 2000);  // Переадресация через 2 секунды
                        } else {
                            console.log('Ошибка при регистрации:', response.errors);
                            signupError.style.display = 'block';
                            const errors = JSON.parse(response.errors);
                            signupError.innerHTML = Object.values(errors).flat().map(e => e.message || e).join('<br>');
                        }
                    } catch (e) {
                        console.error('Ошибка обработки ответа:', e);
                        signupError.style.display = 'block';
                        signupError.innerHTML = 'Произошла ошибка при обработке ответа сервера.';
                    }
                } else {
                    console.error('Ошибка сервера:', xhr.status);
                    signupError.style.display = 'block';
                    signupError.innerHTML = 'Ошибка сервера. Пожалуйста, попробуйте позже.';
                }
            };
            xhr.onerror = function () {
                console.error('Ошибка сети');
                signupError.style.display = 'block';
                signupError.innerHTML = 'Ошибка сети. Пожалуйста, попробуйте позже.';
            };
            xhr.send(formData);
        });
    }
});
