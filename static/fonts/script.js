const formOpenBtn = document.querySelector("#form-open"),
  home = document.querySelector(".home"),
  formContainer = document.querySelector(".form_container"),
  formCloseBtn = document.querySelector(".form_close"),
  signupBtn = document.querySelector("#signup"),
  loginBtn = document.querySelector("#login"),
  pwShowHide = document.querySelectorAll(".pw_hide");
  signupLk = document.querySelector("#signupLink"),
  loginLk = document.querySelector("#loginLink"),

formOpenBtn.addEventListener("click", () => home.classList.add("show"));
formCloseBtn.addEventListener("click", () => home.classList.remove("show"));

signupBtn.addEventListener("click", (e) => {
  e.preventDefault();
  formContainer.classList.add("active");
  register();
});

loginBtn.addEventListener("click", (e) => {
  e.preventDefault();
  formContainer.classList.remove("active");
  login();
})

signupLk.addEventListener("click", (e) => {
  e.preventDefault();
  formContainer.classList.add("active");
});

loginLk.addEventListener("click", (e) => {
  e.preventDefault();
  formContainer.classList.remove("active");
})

pwShowHide.forEach((icon) => {
    icon.addEventListener("click", () => {
      let getPwInput = icon.parentElement.querySelector("input");
      if (getPwInput.type === "password") {
        getPwInput.type = "text";
        icon.classList.replace("uil-eye-slash", "uil-eye");
      } else {
        getPwInput.type = "password";
        icon.classList.replace("uil-eye", "uil-eye-slash");
      }
    });
  });


function login() {
    var username = document.querySelector('.login_form input[type="username"]').value;
    var password = document.querySelector('.login_form input[type="password"]').value;

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username: username, password: password }),
    })
    .then(response => response.json())
    .then(data => {
        // Handle the response from the server
        console.log(data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function register() {
    var email = document.querySelector('.signup_form input[type="email"]').value;
    var username = document.querySelector('.signup_form input[type="username"]').value;
    var password = document.querySelector('.signup_form input[type="password"]').value;

    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: email, username: username, password: password }),
    })
    .then(response => response.json())
    .then(data => {
        // Handle the response from the server
        console.log(data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
