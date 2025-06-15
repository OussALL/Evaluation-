const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');
const message=document.getElementById("message")



registerBtn.addEventListener('click', () => {
    container.classList.add("active");
});

loginBtn.addEventListener('click', () => {
    container.classList.remove("active");
});



message.style.display = "block";
setTimeout(function() {
    message.style.display = "none";
}, 2000); 

