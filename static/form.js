let show = document.querySelector('#show');
let password = document.querySelector('#password');
show.addEventListener('click', function () {
    if (password.type == 'password') {
        password.type = 'text';
    } else {
        password.type = 'password';
    }
});

let generate = document.querySelector('#generate');
generate.addEventListener('click', function () {
    var charset =  "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%&'()*+,^-./:;<=>?[]_`{~}|";
    let pwd = '';
    let length = 15;
    for (let i = 0; i < length; i++) {
        pwd += charset.charAt(Math.floor(Math.random()*charset.length));
    }
    password.value = pwd;
});