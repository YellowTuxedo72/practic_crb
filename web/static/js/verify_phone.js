// document.addEventListener('DOMContentLoaded', () => {
//     const inputs = document.querySelectorAll('.code-input');
//     const fullCodeInput = document.getElementById('full-sms-code');
//     const submitBtn = document.getElementById('submit-verify-btn');
//     const timerSpan = document.getElementById('countdown-timer');
//     const countdownBlock = document.querySelector('.timer-countdown');
//     const resendLink = document.getElementById('resend-link');

//     // Функция поиска первой пустой ячейки
//     function getFirstEmptyInput() {
//         for (let i = 0; i < inputs.length; i++) {
//             if (inputs[i].value === '') {
//                 return inputs[i];
//             }
//         }
//         // Если все заполнены, возвращаем последнюю ячейку
//         return inputs[inputs.length - 1];
//     }

//     // БЕЗОПАСНЫЙ ФОКУС: запрещаем кликать мимо первой пустой ячейки
//     inputs.forEach((input) => {
//         const handleFocus = (e) => {
//             const firstEmpty = getFirstEmptyInput();
//             // Если пользователь пытается сфокусироваться на ячейке, 
//             // которая идет дальше первой пустой, принудительно переносим фокус
//             if (input !== firstEmpty && input.value === '') {
//                 firstEmpty.focus();
//             }
//         };

//         input.addEventListener('focus', handleFocus);
//         input.addEventListener('click', handleFocus); // Для надежности при клике мышкой
//     });

//     // 1. ЛОГИКА ВВОДА СИМВОЛОВ (Автофокус)
//     inputs.forEach((input, index) => {
//         input.addEventListener('input', (e) => {
//             const val = e.target.value;
//             // Разрешаем только цифры
//             e.target.value = val.replace(/\D/g, '');

//             if (e.target.value !== '' && index < inputs.length - 1) {
//                 inputs[index + 1].focus();
//             }
//             checkFullCode();
//         });

//         // Стирание символа назад (Backspace)
//         input.addEventListener('keydown', (e) => {
//             if (e.key === 'Backspace' && e.target.value === '' && index > 0) {
//                 inputs[index - 1].focus();
//             }
//         });
//     });

//     function checkFullCode() {
//         let code = '';
//         inputs.forEach(input => code += input.value);
        
//         fullCodeInput.value = code;

        

//         // Если введены все 6 цифр, активируем кнопку подтверждения
//         if (code.length === 6) {
//             submitBtn.removeAttribute('disabled');
//         } else {
//             submitBtn.setAttribute('disabled', 'true');
//         }
//     }

//     // 2. РАБОТА ТАЙМЕРА (45 секунд)
//     let timeLeft = 45;
//     const timerInterval = setInterval(() => {
//         timeLeft--;
        
//         let minutes = Math.floor(timeLeft / 60);
//         let seconds = timeLeft % 60;

//         minutes = minutes < 10 ? '0' + minutes : minutes;
//         seconds = seconds < 10 ? '0' + seconds : seconds;

//         timerSpan.textContent = `${minutes}:${seconds}`;

//         if (timeLeft <= 0) {
//             clearInterval(timerInterval);
//             countdownBlock.classList.add('hidden');
//             resendLink.classList.remove('hidden');
//         }
//     }, 1000);
// });


document.addEventListener('DOMContentLoaded', () => {
    const inputs = document.querySelectorAll('.code-input');
    const fullCodeInput = document.getElementById('full-sms-code');
    const submitBtn = document.getElementById('submit-verify-btn');
    const timerSpan = document.getElementById('countdown-timer');
    const countdownBlock = document.querySelector('.timer-countdown');
    const resendLink = document.getElementById('resend-link');

    // Функция поиска первой пустой ячейки
    function getFirstEmptyInput() {
        for (let i = 0; i < inputs.length; i++) {
            if (inputs[i].value === '') {
                return inputs[i];
            }
        }
        return inputs[inputs.length - 1];
    }

    // БЕЗОПАСНЫЙ ФОКУС: запрещаем кликать мимо первой пустой ячейки
    inputs.forEach((input) => {
        const handleFocus = (e) => {
            const firstEmpty = getFirstEmptyInput();
            if (input !== firstEmpty && input.value === '') {
                firstEmpty.focus();
            }
        };

        input.addEventListener('focus', handleFocus);
        input.addEventListener('click', handleFocus);
    });

    // 1. ЛОГИКА ВВОДА СИМВОЛОВ (Автофокус вперед)
    inputs.forEach((input, index) => {
        input.addEventListener('input', (e) => {
            const val = e.target.value;
            // Разрешаем строго только цифры
            e.target.value = val.replace(/\D/g, '');

            if (e.target.value !== '' && index < inputs.length - 1) {
                inputs[index + 1].focus();
            }
            checkFullCode();
        });

        // Стирание символа назад (Backspace)
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Backspace' && e.target.value === '' && index > 0) {
                inputs[index - 1].focus();
                inputs[index - 1].value = ''; // Стираем символ в предыдущей ячейке
                checkFullCode();
            }
        });
    });

    function checkFullCode() {
        let code = '';
        inputs.forEach(input => code += input.value);
        
        fullCodeInput.value = code;

        // Если введены все 6 цифр, активируем кнопку подтверждения
        if (code.length === 6) {
            submitBtn.removeAttribute('disabled');
        } else {
            submitBtn.setAttribute('disabled', 'true');
        }
    }

    // 2. РАБОТА ТАЙМЕРА ОБРАТНОГО ОТСЧЕТА (45 секунд)
    let timeLeft = 45;
    const timerInterval = setInterval(() => {
        timeLeft--;
        
        let minutes = Math.floor(timeLeft / 60);
        let seconds = timeLeft % 60;

        minutes = minutes < 10 ? '0' + minutes : minutes;
        seconds = seconds < 10 ? '0' + seconds : seconds;

        if (timerSpan) {
            timerSpan.textContent = `${minutes}:${seconds}`;
        }

        if (timeLeft <= 0) {
            clearInterval(timerInterval);
            if (countdownBlock) countdownBlock.classList.add('hidden');
            if (resendLink) resendLink.classList.remove('hidden');
        }
    }, 1000);
});
