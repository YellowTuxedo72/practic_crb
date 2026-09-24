// document.addEventListener('DOMContentLoaded', () => {
//     const passwordInput = document.getElementById('password');
//     const confirmInput = document.getElementById('password_confirm');
//     const matchError = document.getElementById('match-error');
//     const form = document.getElementById('password-form');
//     const toggleButtons = document.querySelectorAll('.toggle-password');

//     // 1. Показ и скрытие пароля по клику на иконку глаза
//     toggleButtons.forEach(button => {
//         button.addEventListener('click', () => {
//             const targetId = button.getAttribute('data-target');
//             const inputField = document.getElementById(targetId);
//             const svgIcon = button.querySelector('.eye-icon');

//             if (inputField.type === 'password') {
//                 inputField.type = 'text';
//                 svgIcon.style.stroke = '#3b72f3'; // Меняем цвет глаза на синий при показе
//             } else {
//                 inputField.type = 'password';
//                 svgIcon.style.stroke = '#a0aec0'; // Возвращаем серый цвет
//             }
//         });
//     });

//     // 2. Проверка совпадения паролей в реальном времени
//     function validatePasswords() {
//         const passValue = passwordInput.value;
//         const confirmValue = confirmInput.value;

//         // Начинаем проверку, только если в поле подтверждения уже что-то введено
//         if (confirmValue.length > 0) {
//             if (passValue !== confirmValue) {
//                 confirmInput.parentElement.parentElement.classList.add('input-error');
//                 matchError.style.color = '#ef4444'; // Делаем текст ошибки красным
//             } else {
//                 confirmInput.parentElement.parentElement.classList.remove('input-error');
//                 matchError.style.color = '#10b981'; // Подсвечиваем зеленым при полном совпадении
//             }
//         } else {
//             confirmInput.parentElement.parentElement.classList.remove('input-error');
//             matchError.style.color = '#a0aec0'; // Сбрасываем в дефолтный серый
//         }
//     }

//     passwordInput.addEventListener('input', validatePasswords);
//     confirmInput.addEventListener('input', validatePasswords);

//     // Блокировка отправки формы, если пароли не совпадают
//     form.addEventListener('submit', (e) => {
//         if (passwordInput.value !== confirmInput.value) {
//             e.preventDefault();
//             confirmInput.parentElement.parentElement.classList.add('input-error');
//             matchError.style.color = '#ef4444';
//             confirmInput.focus();
//         }
//     });
// });


document.addEventListener('DOMContentLoaded', () => {
    const passwordInput = document.getElementById('password');
    const confirmInput = document.getElementById('password_confirm');
    const matchError = document.getElementById('match-error');
    const form = document.getElementById('password-form');
    const toggleButtons = document.querySelectorAll('.toggle-password');

    // 1. Показ и скрытие пароля по клику на иконку глаза (с перечеркиванием)
    toggleButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetId = button.getAttribute('data-target');
            const inputField = document.getElementById(targetId);
            const svgIcon = button.querySelector('.eye-icon');

            if (inputField.type === 'password') {
                inputField.type = 'text';
                svgIcon.style.stroke = '#3b72f3'; // Меняем цвет глаза на синий
                
                // Добавляем линию перечеркивания глаза для эффекта скрытия
                const lineId = `slash-${targetId}`;
                if (!document.getElementById(lineId)) {
                    const line = document.createElementNS('http://w3.org', 'line');
                    line.setAttribute('id', lineId);
                    line.setAttribute('x1', '1');
                    line.setAttribute('y1', '1');
                    line.setAttribute('x2', '23');
                    line.setAttribute('y2', '23');
                    svgIcon.appendChild(line);
                }
            } else {
                inputField.type = 'password';
                svgIcon.style.stroke = '#a0aec0'; // Возвращаем серый цвет
                
                const slashLine = document.getElementById(`slash-${targetId}`);
                if (slashLine) slashLine.remove();
            }
        });
    });

    // 2. Проверка совпадения паролей в реальном времени
    function validatePasswords() {
        const passValue = passwordInput.value;
        const confirmValue = confirmInput.value;
        // Переключаемся на .parentElement, так как обертка инпута — .input-with-icon
        const container = confirmInput.parentElement;

        if (confirmValue.length > 0) {
            if (passValue !== confirmValue) {
                container.classList.add('input-error');
                matchError.classList.remove('hidden');
                matchError.style.color = '#ef4444'; // Красный при ошибке
            } else {
                container.classList.remove('input-error');
                matchError.classList.remove('hidden');
                matchError.style.color = '#10b981'; // Зеленый при совпадении
            }
        } else {
            container.classList.remove('input-error');
            matchError.classList.add('hidden'); // Прячем ошибку, если поле пустое
        }
    }

    if (passwordInput && confirmInput) {
        passwordInput.addEventListener('input', validatePasswords);
        confirmInput.addEventListener('input', validatePasswords);
    }

    // 3. Блокировка отправки формы при несовпадении
    if (form) {
        form.addEventListener('submit', (e) => {
            if (passwordInput.value !== confirmInput.value) {
                e.preventDefault();
                confirmInput.parentElement.classList.add('input-error');
                matchError.classList.remove('hidden');
                matchError.style.color = '#ef4444';
                confirmInput.focus();
            }
        });
    }

    // 4. Подсветка левых иконок (замочков) при фокусе на полях
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
