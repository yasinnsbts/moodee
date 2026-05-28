console.log("Ладно loaded");
(function () {
    const savedTheme = localStorage.getItem("ladno-theme");

    if (savedTheme === "dark") {
        document.documentElement.classList.add("theme-dark-preload");
    }
})();

document.addEventListener("DOMContentLoaded", function () {
    const themeSelect = document.querySelector('select[name="theme"]');

    function applyTheme(theme) {
        const normalizedTheme = theme === "dark" ? "dark" : "light";
        const isDark = normalizedTheme === "dark";

        document.body.classList.toggle("theme-dark", isDark);
        document.body.classList.toggle("theme-light", !isDark);

        localStorage.setItem("ladno-theme", normalizedTheme);
    }

    /*
      Если на странице есть select темы, он главный.
      Это важно для profile.html: пользователь меняет select —
      тема должна меняться сразу, даже без сохранения.
    */
    if (themeSelect) {
        applyTheme(themeSelect.value);

        themeSelect.addEventListener("change", function () {
            applyTheme(themeSelect.value);
        });

        return;
    }

    /*
      На остальных страницах select нет, поэтому берём тему из localStorage.
    */
    const savedTheme = localStorage.getItem("ladno-theme");

    if (savedTheme === "dark" || savedTheme === "light") {
        applyTheme(savedTheme);
    }
});
document.addEventListener("DOMContentLoaded", function () {
    const themeSelect = document.querySelector('select[name="theme"]');

    if (!themeSelect) {
        return;
    }

    function applyTheme(theme) {
        const isDark = theme === "dark";

        document.body.classList.toggle("theme-dark", isDark);
        document.body.classList.toggle("theme-light", !isDark);
    }

    applyTheme(themeSelect.value);

    themeSelect.addEventListener("change", function () {
        applyTheme(themeSelect.value);
    });
});