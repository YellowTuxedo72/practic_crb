document.addEventListener('DOMContentLoaded', () => {
    const selectableServices = document.querySelectorAll('.service-row-card.selectable-service');
    const hiddenServiceInput = document.getElementById('selected-service-id');
    const submitBtn = document.getElementById('submit-btn');

    selectableServices.forEach(card => {
        card.addEventListener('click', () => {
            const serviceId = card.getAttribute('data-service-id');

            selectableServices.forEach(c => c.classList.remove('selected-service'));
            card.classList.add('selected-service');

            if (hiddenServiceInput) {
                hiddenServiceInput.value = serviceId;
            }

            if (submitBtn) {
                submitBtn.removeAttribute('disabled');
            }
        });
    });
});


// Логика активации кнопки "Далее" при выборе времени
const timeRadioButtons = document.querySelectorAll('.time-option input[type="radio"]');
const timeSubmitBtn = document.getElementById('time-submit-btn');

if (timeRadioButtons.length > 0 && timeSubmitBtn) {
    timeRadioButtons.forEach(radio => {
        // Проверяем состояние при загрузке (если бэкенд уже вернул выбранную радиокнопку)
        if (radio.checked) {
            timeSubmitBtn.removeAttribute('disabled');
        }

        // Слушаем переключение радиокнопок пользователем
        radio.addEventListener('change', () => {
            if (radio.checked) {
                timeSubmitBtn.removeAttribute('disabled');
            }
        });
    });
}
