document.addEventListener('DOMContentLoaded', function() {
  
  // Плавное переключение между формами
  const switchToSignup = document.getElementById('switch-to-signup');
  const switchToSignin = document.getElementById('switch-to-signin');
  
  function scrollToCard(cardElement) {
    if (window.innerWidth <= 780) {
      cardElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
    } else {
      cardElement.style.transition = 'all 0.2s';
      cardElement.style.boxShadow = '0 0 0 2px #6366f1, 0 10px 25px -5px rgba(0,0,0,0.1)';
      setTimeout(() => {
        cardElement.style.boxShadow = '';
      }, 800);
    }
  }
  
  if (switchToSignup) {
    switchToSignup.addEventListener('click', (e) => {
      e.preventDefault();
      const signupCard = document.querySelector('.auth-card:last-child');
      scrollToCard(signupCard);
    });
  }
  
  if (switchToSignin) {
    switchToSignin.addEventListener('click', (e) => {
      e.preventDefault();
      const signinCard = document.querySelector('.auth-card:first-child');
      scrollToCard(signinCard);
    });
  }
  
  // Подтверждение пароля на клиенте (регистрация)
  const signupForm = document.getElementById('signup-form');
  if (signupForm) {
    const passwordField = signupForm.querySelector('#id_password1');
    const confirmField = signupForm.querySelector('#id_password2');
    
    if (passwordField && confirmField) {
      function checkPasswordMatch() {
        if (passwordField.value !== confirmField.value) {
          confirmField.setCustomValidity('Пароли не совпадают');
        } else {
          confirmField.setCustomValidity('');
        }
      }
      passwordField.addEventListener('change', checkPasswordMatch);
      confirmField.addEventListener('keyup', checkPasswordMatch);
    }
  }
  
  // Убираем сообщения об ошибках при вводе
  const formInputs = document.querySelectorAll('.input-field');
  formInputs.forEach(input => {
    input.addEventListener('input', function() {
      const errorDiv = this.parentElement.querySelector('.errorlist');
      if (errorDiv) errorDiv.style.display = 'none';
    });
  });
  
  console.log('✅ Moodee: интерфейс загружен');
});