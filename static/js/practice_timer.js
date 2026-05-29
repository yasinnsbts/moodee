document.addEventListener("DOMContentLoaded", function () {
    const actionElements = Array.from(
        document.querySelectorAll("[data-practice-duration], button, a")
    ).filter(function (element) {
        return (
            element.dataset.practiceDuration ||
            element.textContent.trim().toLowerCase() === "выполнить"
        );
    });

    if (actionElements.length === 0) {
        return;
    }

    let timerInterval = null;
    let remainingSeconds = 0;
    let initialSeconds = 0;
    let musicEnabled = true;

    const practiceMusic = new Audio("/static/audio/practice_calm.mp3");
    practiceMusic.loop = true;
    practiceMusic.volume = 0.25;

    const modal = document.createElement("div");
    modal.className = "practice-timer-modal";
    modal.setAttribute("aria-hidden", "true");

    modal.innerHTML = `
        <div class="practice-timer-backdrop" data-practice-close="true"></div>

        <div class="practice-timer-dialog" role="dialog" aria-modal="true" aria-labelledby="practice-timer-title">
            <button type="button" class="practice-timer-close" data-practice-close="true" aria-label="Закрыть">
                ×
            </button>

            <p class="practice-timer-label">Практика</p>
            <h2 id="practice-timer-title">Дыхательная практика</h2>

            <p class="practice-timer-duration"></p>

            <div class="practice-timer-instruction"></div>

            <div class="practice-timer-time" aria-live="polite">
                00:00
            </div>

            <div class="practice-timer-progress">
                <div class="practice-timer-progress-bar"></div>
            </div>

            <div class="practice-timer-actions">
                <button type="button" class="practice-timer-start">Старт</button>
                <button type="button" class="practice-timer-pause">Пауза</button>
                <button type="button" class="practice-timer-reset">Сброс</button>
            </div>

            <button type="button" class="practice-music-toggle">
                Музыка: вкл
            </button>

            <p class="practice-timer-note">
                Если упражнение вызывает дискомфорт, остановитесь и вернитесь к обычному дыханию.
            </p>
        </div>
    `;

    document.body.appendChild(modal);

    const titleElement = modal.querySelector("#practice-timer-title");
    const durationElement = modal.querySelector(".practice-timer-duration");
    const instructionElement = modal.querySelector(".practice-timer-instruction");
    const timeElement = modal.querySelector(".practice-timer-time");
    const progressBar = modal.querySelector(".practice-timer-progress-bar");
    const startButton = modal.querySelector(".practice-timer-start");
    const pauseButton = modal.querySelector(".practice-timer-pause");
    const resetButton = modal.querySelector(".practice-timer-reset");
    const musicToggleButton = modal.querySelector(".practice-music-toggle");

    function findPracticeCard(element) {
        return (
            element.closest(".card") ||
            element.closest(".practice-card") ||
            element.closest("article") ||
            element.closest("li") ||
            element.parentElement
        );
    }

    function fallbackTitle(card) {
        if (!card) {
            return "Дыхательная практика";
        }

        const title = card.querySelector("h1, h2, h3, h4, .practice-title, .card-title");

        if (title && title.textContent.trim()) {
            return title.textContent.trim();
        }

        return "Дыхательная практика";
    }

    function fallbackDurationMinutes(card) {
        if (!card) {
            return 2;
        }

        const text = card.textContent;

        const patterns = [
            /(\d+)\s*минут/i,
            /(\d+)\s*минуты/i,
            /(\d+)\s*минута/i,
            /(\d+)\s*мин\./i,
            /(\d+)\s*мин/i
        ];

        for (const pattern of patterns) {
            const match = text.match(pattern);

            if (match && match[1]) {
                const minutes = parseInt(match[1], 10);

                if (!Number.isNaN(minutes) && minutes > 0) {
                    return minutes;
                }
            }
        }

        return 2;
    }

    function fallbackInstruction(card) {
        if (!card) {
            return "Следуйте инструкции в карточке и выполняйте практику в комфортном темпе.";
        }

        const instruction = card.querySelector(
            ".practice-instruction, .instruction, [data-practice-instruction]"
        );

        if (instruction && instruction.textContent.trim()) {
            return instruction.textContent.trim();
        }

        const paragraphs = Array.from(card.querySelectorAll("p"))
            .map(function (item) {
                return item.textContent.trim();
            })
            .filter(Boolean);

        if (paragraphs.length > 0) {
            return paragraphs[paragraphs.length - 1];
        }

        return "Следуйте инструкции в карточке и выполняйте практику в комфортном темпе.";
    }

    function getPracticeData(element) {
        const card = findPracticeCard(element);

        const title = element.dataset.practiceTitle || fallbackTitle(card);

        const rawDuration = element.dataset.practiceDuration;
        let durationMinutes = parseInt(rawDuration, 10);

        if (Number.isNaN(durationMinutes) || durationMinutes <= 0) {
            durationMinutes = fallbackDurationMinutes(card);
        }

        const instruction =
            element.dataset.practiceInstruction ||
            fallbackInstruction(card);

        return {
            title: title,
            durationMinutes: durationMinutes,
            instruction: instruction
        };
    }

    function formatDurationText(minutes) {
        if (minutes === 1) {
            return "Длительность: 1 минута";
        }

        if (minutes >= 2 && minutes <= 4) {
            return "Длительность: " + minutes + " минуты";
        }

        return "Длительность: " + minutes + " минут";
    }

    function formatTime(seconds) {
        const minutes = Math.floor(seconds / 60);
        const restSeconds = seconds % 60;

        return String(minutes).padStart(2, "0") + ":" + String(restSeconds).padStart(2, "0");
    }

    function renderTimer() {
        timeElement.textContent = formatTime(remainingSeconds);

        if (initialSeconds > 0) {
            const progress = ((initialSeconds - remainingSeconds) / initialSeconds) * 100;
            progressBar.style.width = Math.min(Math.max(progress, 0), 100) + "%";
        } else {
            progressBar.style.width = "0%";
        }
    }

    function playMusic() {
        if (!musicEnabled) {
            return;
        }

        practiceMusic.play().catch(function () {
            // Браузер может заблокировать звук, если пользователь ещё не взаимодействовал со страницей.
        });
    }

    function pauseMusic() {
        practiceMusic.pause();
    }

    function stopMusic() {
        practiceMusic.pause();
        practiceMusic.currentTime = 0;
    }

    function stopTimer() {
        if (timerInterval) {
            clearInterval(timerInterval);
            timerInterval = null;
        }
    }

    function startTimer() {
        if (remainingSeconds <= 0) {
            resetTimer();
        }

        if (timerInterval) {
            return;
        }

        playMusic();

        timerInterval = setInterval(function () {
            remainingSeconds -= 1;

            if (remainingSeconds <= 0) {
                remainingSeconds = 0;
                stopTimer();
                stopMusic();
                startButton.textContent = "Повторить";
            }

            renderTimer();
        }, 1000);
    }

    function pauseTimer() {
        stopTimer();
        pauseMusic();
    }

    function resetTimer() {
        stopTimer();
        stopMusic();
        remainingSeconds = initialSeconds;
        startButton.textContent = "Старт";
        renderTimer();
    }

    function openModal(element) {
        const data = getPracticeData(element);

        stopMusic();

        initialSeconds = data.durationMinutes * 60;
        remainingSeconds = initialSeconds;

        titleElement.textContent = data.title;
        durationElement.textContent = formatDurationText(data.durationMinutes);
        instructionElement.textContent = data.instruction;
        startButton.textContent = "Старт";

        renderTimer();

        modal.classList.add("is-open");
        modal.setAttribute("aria-hidden", "false");
        document.body.classList.add("practice-timer-open");
    }

    function closeModal() {
        stopTimer();
        stopMusic();
        modal.classList.remove("is-open");
        modal.setAttribute("aria-hidden", "true");
        document.body.classList.remove("practice-timer-open");
    }

    actionElements.forEach(function (element) {
        element.addEventListener("click", function (event) {
            event.preventDefault();
            openModal(element);
        });
    });

    startButton.addEventListener("click", startTimer);
    pauseButton.addEventListener("click", pauseTimer);
    resetButton.addEventListener("click", resetTimer);

    musicToggleButton.addEventListener("click", function () {
        musicEnabled = !musicEnabled;

        if (musicEnabled) {
            musicToggleButton.textContent = "Музыка: вкл";

            if (timerInterval) {
                playMusic();
            }
        } else {
            musicToggleButton.textContent = "Музыка: выкл";
            pauseMusic();
        }
    });

    modal.addEventListener("click", function (event) {
        if (event.target.dataset.practiceClose === "true") {
            closeModal();
        }
    });

    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape" && modal.classList.contains("is-open")) {
            closeModal();
        }
    });
});
