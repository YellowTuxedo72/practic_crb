// document.addEventListener('DOMContentLoaded', () => {
//     const phoneInput = document.getElementById('phone');
//     const passwordInput = document.getElementById('password');
//     const togglePasswordBtn = document.querySelector('.toggle-password');

//     // 1. Показ / Скрытие пароля
//     if (togglePasswordBtn && passwordInput) {
//         togglePasswordBtn.addEventListener('click', () => {
//             const svgIcon = togglePasswordBtn.querySelector('.eye-icon');
//             if (passwordInput.type === 'password') {
//                 passwordInput.type = 'text';
//                 svgIcon.style.stroke = '#3b72f3'; // Синеет при активации
//             } else {
//                 passwordInput.type = 'password';
//                 svgIcon.style.stroke = '#a0aec0';
//             }
//         });
//     }

//     // 2. Маска ввода для телефона (+7 (XXX) XXX-XX-XX)
//     if (phoneInput) {
//         phoneInput.addEventListener('input', (e) => {
//             let value = e.target.value.replace(/\D/g, '');
            
//             if (value.startsWith('7') || value.startsWith('8')) {
//                 value = value.substring(1);
//             }
//             if (value.length > 10) value = value.slice(0, 10);

//             let formatted = '+7 ';
//             if (value.length > 0) formatted += '(' + value.substring(0, 3);
//             if (value.length > 3) formatted += ') ' + value.substring(3, 6);
//             if (value.length > 6) formatted += '-' + value.substring(6, 8);
//             if (value.length > 8) formatted += '-' + value.substring(8, 10);
            
//             e.target.value = value.length === 0 ? '' : formatted;
//         });
//     }

//     // 3. Подсветка внутренних иконок при фокусе на полях
//     const inputs = document.querySelectorAll('.input-with-icon input');
//     inputs.forEach(input => {
//         const icon = input.parentElement.querySelector('.field-icon svg');
//         if (icon) {
//             input.addEventListener('focus', () => {
//                 icon.style.stroke = '#3b72f3';
//             });
//             input.addEventListener('blur', () => {
//                 icon.style.stroke = '#a0aec0';
//             });
//         }
//     });
// });


document.addEventListener('DOMContentLoaded', () => {
    const phoneInput = document.getElementById('phone');
    const passwordInput = document.getElementById('password');
    const togglePasswordBtn = document.querySelector('.toggle-password');

    // 1. Показ / Скрытие пароля с динамической сменой иконки (глаз / перечеркнутый глаз)
    if (togglePasswordBtn && passwordInput) {
        togglePasswordBtn.addEventListener('click', () => {
            const svgIcon = togglePasswordBtn.querySelector('.eye-icon');
            
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                // Окрашиваем в синий цвет и меняем иконку на перечеркнутый глаз (добавляем линию косой черты)
                svgIcon.style.stroke = '#3b72f3';
                if (!document.getElementById('eye-slash-line')) {
                    const line = document.createElementNS('http://w3.org', 'line');
                    line.setAttribute('id', 'eye-slash-line');
                    line.setAttribute('x1', '1');
                    line.setAttribute('y1', '1');
                    line.setAttribute('x2', '23');
                    line.setAttribute('y2', '23');
                    svgIcon.appendChild(line);
                }
            } else {
                passwordInput.type = 'password';
                svgIcon.style.stroke = '#a0aec0';
                const slashLine = document.getElementById('eye-slash-line');
                if (slashLine) slashLine.remove();
            }
        });
    }

    // 2. Функция форматирования номера по маске +7 (XXX) XXX-XX-XX
    function formatPhoneNumber(inputElement) {
        let value = inputElement.value.replace(/\D/g, '');
        
        // Обработка первой семерки или восьмерки
        if (value.startsWith('7') || value.startsWith('8')) {
            value = value.substring(1);
        }
        if (value.length > 10) value = value.slice(0, 10);

        let formatted = '+7 ';
        if (value.length > 0) formatted += '(' + value.substring(0, 3);
        if (value.length > 3) formatted += ') ' + value.substring(3, 6);
        if (value.length > 6) formatted += '-' + value.substring(6, 8);
        if (value.length > 8) formatted += '-' + value.substring(8, 10);
        
        inputElement.value = value.length === 0 ? '' : formatted;
    }

    if (phoneInput) {
        // Форматируем сразу при загрузке (если Django вернул в поле старое значение после ошибки)
        if (phoneInput.value) {
            formatPhoneNumber(phoneInput);
        }

        // Форматирование при вводе
        phoneInput.addEventListener('input', (e) => {
            formatPhoneNumber(e.target);
        });

        // Корректная обработка клавиши Backspace, чтобы маска не "застревала" на скобках и дефисах
        phoneInput.addEventListener('keydown', (e) => {
            if (e.key === 'Backspace') {
                const value = e.target.value.replace(/\D/g, '');
                // Если осталась только семерка, при нажатии Backspace полностью очищаем поле
                if (value.length <= 1) {
                    e.target.value = '';
                }
            }
        });
    }

    // 3. Подсветка внутренних иконок при фокусе на полях
    const inputs = document.querySelectorAll('.input-with-icon input');
    inputs.forEach(input => {
        const icon = input.parentElement.querySelector('.field-icon svg');
        if (icon) {
            input.addEventListener('focus', () => {
                icon.style.stroke = '#3b72f3';
                icon.style.transition = 'stroke 0.2s ease';
            });
            input.addEventListener('blur', () => {
                icon.style.stroke = '#a0aec0';
            });
        }
    });
});
