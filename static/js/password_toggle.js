document.addEventListener("DOMContentLoaded", function () {
    const passwordFields = document.querySelectorAll('input[type="password"]');

    passwordFields.forEach(function (field) {
        if (field.dataset.passwordToggleReady === "true") {
            return;
        }

        field.dataset.passwordToggleReady = "true";

        const wrapper = document.createElement("div");
        wrapper.className = "password-toggle-wrapper";

        field.parentNode.insertBefore(wrapper, field);
        wrapper.appendChild(field);

        const button = document.createElement("button");
        button.type = "button";
        button.className = "password-toggle-button";
        button.textContent = "Показать";
        button.setAttribute("aria-label", "Показать пароль");

        button.addEventListener("click", function () {
            const isHidden = field.type === "password";

            field.type = isHidden ? "text" : "password";
            button.textContent = isHidden ? "Скрыть" : "Показать";
            button.setAttribute(
                "aria-label",
                isHidden ? "Скрыть пароль" : "Показать пароль"
            );
        });

        wrapper.appendChild(button);
    });
});
