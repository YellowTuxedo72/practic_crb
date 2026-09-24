document.addEventListener('DOMContentLoaded', () => {
    const menuLinks = document.querySelectorAll('.menu-link:not(.logout-link)');
    const tabContents = document.querySelectorAll('.cabinet-tab-content'); // Успешно найдет и теги <section>
    
    // Внутренние под-разделы Главного экрана
    const subviewDashboard = document.getElementById('subview-dashboard');
    const subviewAllUpcoming = document.getElementById('subview-all-upcoming');

    function switchTab(targetTabId) {
        if (!targetTabId) return;

        // Прячем все основные секции/вкладки
        tabContents.forEach(content => {
            content.classList.add('hidden');
        });

        // Показываем выбранную секцию
        const activeContent = document.getElementById(targetTabId);
        if (activeContent) {
            activeContent.classList.remove('hidden');
        }

        // Если пользователь переключается на вкладку Главной из сайдбара,
        // сбрасываем вид под-разделов на базовый дэшборд (показываем баннер)
        if (targetTabId === 'tab-main' || targetTabId === 'main-tab') { // Проверьте точный ID вашей главной секции
            if (subviewDashboard) subviewDashboard.classList.remove('hidden');
            if (subviewAllUpcoming) subviewAllUpcoming.classList.add('hidden');
        }

        // Убираем active у всех пунктов меню
        menuLinks.forEach(item => item.classList.remove('active'));

        // Добавляем active выбранному
        menuLinks.forEach(link => {
            if (link.getAttribute('data-tab') === targetTabId) {
                link.classList.add('active');
            }
        });

        // Запоминаем текущую вкладку
        localStorage.setItem('patientCabinetActiveTab', targetTabId);
    }

    // Переключение вкладок из сайдбара
    menuLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetTab = link.getAttribute('data-tab');
            switchTab(targetTab);
        });
    });


        // =========================================================
    // ЛОГИКА ВНУТРЕННЕГО ПЕРЕКЛЮЧЕНИЯ "ВСЕ ЗАПИСИ" С АНИМАЦИЕЙ
    // =========================================================
    const btnShowAllUpcoming = document.getElementById('trigger-show-all-upcoming');
    const btnBackToDashboard = document.getElementById('trigger-back-to-dashboard');

    if (btnShowAllUpcoming && subviewDashboard && subviewAllUpcoming) {
        btnShowAllUpcoming.addEventListener('click', (e) => {
            e.preventDefault();
            
            // 1. Скрываем базовый дэшборд
            subviewDashboard.classList.add('hidden');
            
            // 2. Сбрасываем и запускаем анимацию для списка будущих записей
            subviewAllUpcoming.style.animation = 'none';
            subviewAllUpcoming.offsetHeight; // Специфический хак для принудительного рендеринга в браузере
            subviewAllUpcoming.style.animation = '';
            
            // 3. Показываем список будущих записей
            subviewAllUpcoming.classList.remove('hidden');
            
            // 4. Плавно поднимаем экран наверх
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    if (btnBackToDashboard && subviewDashboard && subviewAllUpcoming) {
        btnBackToDashboard.addEventListener('click', (e) => {
            e.preventDefault();
            
            // 1. Скрываем список будущих записей
            subviewAllUpcoming.classList.add('hidden');
            
            // 2. Сбрасываем и запускаем анимацию для базового дэшборд-экрана
            subviewDashboard.style.animation = 'none';
            subviewDashboard.offsetHeight; // Специфический хак для принудительного рендеринга в браузере
            subviewDashboard.style.animation = '';
            
            // 3. Возвращаем базовый экран обратно
            subviewDashboard.classList.remove('hidden');
        });
    }


    // Восстанавливаем вкладку после F5
    const savedTab = localStorage.getItem('patientCabinetActiveTab');
    if (savedTab && document.getElementById(savedTab)) {
        switchTab(savedTab);
    } else {
        // Если записей в localStorage нет, открываем главную секцию
        // Убедитесь, что ID совпадает с вашим тегом <section id="...">
        const defaultTab = document.getElementById('tab-main') ? 'tab-main' : 'main-tab';
        switchTab(defaultTab);
    }
});




// ИСПРАВЛЕННЫЙ ФИЛЬТР ДЛЯ НОВЫХ КАРТОЧЕК
document.querySelectorAll(".medical-filter").forEach(button => {
    button.addEventListener("click", () => {
        const filter = button.dataset.filter;

        document.querySelectorAll(".medical-filter").forEach(btn => {
            btn.classList.remove("active");
        });

        button.classList.add("active");

        document.querySelectorAll(".medical-record-card").forEach(record => {
            const type = record.dataset.type;

            record.style.display =
                filter === "all" || type === filter
                    ? ""
                    : "none";
        });
    });
});


// =========================================================
// ЛОГИКА МОДАЛЬНОГО ОКНА ОТМЕНЫ ЗАПИСИ
// =========================================================

const cancelModal = document.getElementById(
    "cancel-appointment-modal"
);

const btnCloseModal = document.getElementById(
    "btn-close-cancel-modal"
);

const modalOverlay = document.querySelector(
    ".custom-modal-overlay"
);

const cancelForm = document.getElementById(
    "cancel-appointment-form"
);

// Открытие модального окна
document.body.addEventListener("click", (e) => {
    const trigger = e.target.closest(
        ".trigger-open-cancel-modal"
    );

    if (!trigger) {
        return;
    }

    e.preventDefault();

    const appointmentId = trigger.dataset.appointmentId;

    if (!appointmentId) {
        return;
    }

    if (cancelForm) {
        cancelForm.action =
            `/cabinet/appointments/${appointmentId}/cancel/`;
    }

    if (cancelModal) {
        cancelModal.classList.remove("hidden");
    }
});

// Закрытие модального окна
function closeCancelModal() {
    if (cancelModal) {
        cancelModal.classList.add("hidden");
    }
}

if (btnCloseModal) {
    btnCloseModal.addEventListener(
        "click",
        closeCancelModal
    );
}

if (modalOverlay) {
    modalOverlay.addEventListener(
        "click",
        closeCancelModal
    );
}



// =========================================================
// АККОРДЕОН МЕДИЦИНСКИХ ЗАПИСЕЙ
// + ДЕТАЛИ АРХИВНЫХ ЗАПИСЕЙ
// + ДЕТАЛИ БУДУЩИХ ЗАПИСЕЙ
// =========================================================

document.body.addEventListener("click", async (event) => {
    const button = event.target.closest(
        ".medical-accordion-toggle"
    );

    if (!button) {
        return;
    }

    event.preventDefault();

    const record = button.closest(
        ".medical-record-card"
    );

    if (!record) {
        return;
    }

    const details = record.querySelector(
        ".medical-details-collapse"
    );

    if (!details) {
        return;
    }

    const buttonText = button.querySelector(
        "span:first-child"
    );

    const arrow = button.querySelector(
        ".btn-arrow"
    );

    const isOpen = !details.classList.contains(
        "hidden"
    );


    // =====================================================
    // ЗАКРЫТИЕ ТЕКУЩЕЙ КАРТОЧКИ
    // =====================================================

    if (isOpen) {
        details.classList.add("hidden");

        if (buttonText) {
            buttonText.textContent = "Подробнее";
        }

        if (arrow) {
            arrow.style.transform = "";
        }

        return;
    }


    // =====================================================
    // ЗАКРЫВАЕМ ОСТАЛЬНЫЕ КАРТОЧКИ
    // =====================================================

    document
        .querySelectorAll(".medical-record-card")
        .forEach(otherRecord => {

            if (otherRecord === record) {
                return;
            }

            const otherDetails =
                otherRecord.querySelector(
                    ".medical-details-collapse"
                );

            const otherButton =
                otherRecord.querySelector(
                    ".medical-accordion-toggle"
                );

            if (otherDetails) {
                otherDetails.classList.add("hidden");
            }

            if (otherButton) {
                const otherText =
                    otherButton.querySelector(
                        "span:first-child"
                    );

                const otherArrow =
                    otherButton.querySelector(
                        ".btn-arrow"
                    );

                if (otherText) {
                    otherText.textContent =
                        "Подробнее";
                }

                if (otherArrow) {
                    otherArrow.style.transform = "";
                }
            }
        });


    // =====================================================
    // ОТКРЫВАЕМ ТЕКУЩУЮ КАРТОЧКУ
    // =====================================================

    details.classList.remove("hidden");

    if (buttonText) {
        buttonText.textContent = "Свернуть";
    }

    if (arrow) {
        arrow.style.transform =
            "rotate(90deg)";
    }


    // =====================================================
    // ПРОВЕРЯЕМ, ЕСТЬ ЛИ ID МЕДИЦИНСКОЙ ЗАПИСИ
    // =====================================================

    const recordId = record.dataset.recordId;

    // Если ID нет — это будущая запись.
    // Её детали уже находятся в HTML,
    // поэтому больше ничего делать не нужно.
    if (!recordId) {
        return;
    }


    // =====================================================
    // НИЖЕ — ЛОГИКА ТОЛЬКО ДЛЯ АРХИВНЫХ ЗАПИСЕЙ
    // =====================================================

    const content = record.querySelector(
        ".medical-details-content"
    );

    if (!content) {
        return;
    }


    // Если уже загружали — повторный запрос не нужен
    if (
        record.dataset.detailsLoaded ===
        "true"
    ) {
        return;
    }


    // Показываем загрузку
    content.textContent = "Загрузка...";


    try {
        console.log(
            "Загрузка деталей медицинской записи:",
            recordId
        );

        const response = await fetch(
            `/cabinet/medical-records/${recordId}/`
        );


        if (!response.ok) {
            throw new Error(
                `HTTP ${response.status}`
            );
        }


        const data =
            await response.json();


        console.log(
            "Детали медицинской записи:",
            data
        );


        content.innerHTML = "";


        // =================================================
        // РЕЗУЛЬТАТ
        // =================================================

        if (data.result) {
            const resultRow =
                document.createElement("div");

            resultRow.className =
                "detail-row";

            resultRow.innerHTML = `
                <strong>Результат:</strong>
                ${data.result}
            `;

            content.appendChild(
                resultRow
            );
        }


        // =================================================
        // ЗАКЛЮЧЕНИЕ
        // =================================================

        if (data.conclusion) {
            const conclusionRow =
                document.createElement("div");

            conclusionRow.className =
                "detail-row";

            conclusionRow.innerHTML = `
                <strong>Заключение:</strong>
                ${data.conclusion}
            `;

            content.appendChild(
                conclusionRow
            );
        }


        // =================================================
        // ПРОТОКОЛ
        // =================================================

        if (data.protocol) {
            const protocolRow =
                document.createElement("div");

            protocolRow.className =
                "detail-row";

            protocolRow.innerHTML = `
                <strong>Протокол:</strong>
                ${data.protocol}
            `;

            content.appendChild(
                protocolRow
            );
        }


        // Если данных нет
        if (!content.innerHTML.trim()) {
            content.textContent =
                "Подробная информация отсутствует.";
        }


        record.dataset.detailsLoaded =
            "true";


    } catch (error) {

        console.error(
            "Ошибка загрузки медицинской записи:",
            error
        );

        content.textContent =
            "Не удалось загрузить подробности записи.";
    }
});