const register = document.getElementById("register");
const overlay = document.querySelector(".overlay");
const showBtn = document.querySelector(".btn");
const closeBtn = document.querySelector(".close-btn");

showBtn.addEventListener("click", () => register.classList.add("active"));
overlay.addEventListener("click", () => register.classList.remove("active"));
closeBtn.addEventListener("click", () =>
    register.classList.remove("active")
  );