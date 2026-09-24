// document.addEventListener("DOMContentLoaded", () => {
//   const snilsInput = document.getElementById("snils");
//   const phoneInput = document.getElementById("phone");
//   const dobInput = document.getElementById("dob");

//   // Находим дату ровно 18 лет назад от сегодняшнего дня
//   const now = new Date();
//   now.setFullYear(now.getFullYear() - 18);
//   const maxDate18 = now.toISOString().split("T")[0];

//   // Устанавливаем максимальную доступную дату в календаре
//   dobInput.setAttribute("max", maxDate18);
//   // Маска для СНИЛС (000-000-000 00)
//   snilsInput.addEventListener("input", (e) => {
//     let value = e.target.value.replace(/\D/g, "");
//     if (value.length > 11) value = value.slice(0, 11);

//     let formatted = "";
//     if (value.length > 0) formatted += value.substring(0, 3);
//     if (value.length > 3) formatted += "-" + value.substring(3, 6);
//     if (value.length > 6) formatted += "-" + value.substring(6, 9);
//     if (value.length > 9) formatted += " " + value.substring(9, 11);

//     e.target.value = formatted;
//   });

//   // Маска для телефона (+7 (XXX) XXX-XX-XX)
//   // Маска для телефона (+7 (XXX) XXX-XX-XX) - ИСПРАВЛЕННАЯ
//   phoneInput.addEventListener("input", (e) => {
//     // Оставляем только цифры
//     let value = e.target.value.replace(/\D/g, "");

//     // Если пользователь ничего не ввел, очищаем поле
//     if (value.length === 0) {
//       e.target.value = "";
//       return;
//     }

//     // УМНАЯ КОРРЕКЦИЯ ПЕРВОЙ ЦИФРЫ:
//     // Если вводят 8914..., меняем 8 на 7
//     if (value.startsWith("8")) {
//       value = "7" + value.substring(1);
//     }
//     // Если начинают вводить сразу с девятки 914..., дописываем 7 в начало
//     else if (!value.startsWith("7") && value.length > 0) {
//       value = "7" + value;
//     }

//     // Ограничиваем длину до 11 цифр (включая семерку)
//     if (value.length > 11) value = value.slice(0, 11);

//     // Форматируем строку по ходу ввода (начиная со второй цифры)
//     let formatted = "+7";
//     if (value.length > 1) formatted += " (" + value.substring(1, 4);
//     if (value.length > 4) formatted += ") " + value.substring(4, 7);
//     if (value.length > 7) formatted += "-" + value.substring(7, 9);
//     if (value.length > 9) formatted += "-" + value.substring(9, 11);

//     e.target.value = formatted;
//   });
// });


document.addEventListener("DOMContentLoaded", () => {
  const snilsInput = document.getElementById("snils");
  const phoneInput = document.getElementById("phone");
  const dobInput = document.getElementById("dob");

  // 1. Ограничение календаря (минус 18 лет)
  if (dobInput) {
    const now = new Date();
    now.setFullYear(now.getFullYear() - 18);
    const maxDate18 = now.toISOString().split("T")[0];
    dobInput.setAttribute("max", maxDate18);
  }

  // 2. Маска для СНИЛС (000-000-000 00)
  if (snilsInput) {
    snilsInput.addEventListener("input", (e) => {
      let value = e.target.value.replace(/\D/g, "");
      if (value.length > 11) value = value.slice(0, 11);

      let formatted = "";
      if (value.length > 0) formatted += value.substring(0, 3);
      if (value.length > 3) formatted += "-" + value.substring(3, 6);
      if (value.length > 6) formatted += "-" + value.substring(6, 9);
      if (value.length > 9) formatted += " " + value.substring(9, 11);

      e.target.value = formatted;
    });
  }

  // 3. Маска для телефона (+7 (XXX) XXX-XX-XX)
  if (phoneInput) {
    phoneInput.addEventListener("input", (e) => {
      let value = e.target.value.replace(/\D/g, "");

      if (value.length === 0) {
        e.target.value = "";
        return;
      }

      if (value.startsWith("8")) {
        value = "7" + value.substring(1);
      } else if (!value.startsWith("7") && value.length > 0) {
        value = "7" + value;
      }

      if (value.length > 11) value = value.slice(0, 11);

      let formatted = "+7";
      if (value.length > 1) formatted += " (" + value.substring(1, 4);
      if (value.length > 4) formatted += ") " + value.substring(4, 7);
      if (value.length > 7) formatted += "-" + value.substring(7, 9);
      if (value.length > 9) formatted += "-" + value.substring(9, 11);

      e.target.value = formatted;
    });
  }

  // 4. Динамическая подсветка иконок при фокусе для всех инпутов регистрации
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
