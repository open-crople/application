// Function to toggle password visibility
function togglePasswordVisibility() {
    var passwordField = document.getElementById('password');
    var eyeIcons = document.querySelectorAll('.eyeblock');

    if (passwordField.type === 'password') {
        passwordField.type = 'text';
        eyeIcons.forEach(function (icon) {
            icon.src = '../static/images/eyeopen.png';
        });
    } else {
        passwordField.type = 'password';
        eyeIcons.forEach(function (icon) {
            icon.src = '../static/images/eyeblock.png';
        });
    }
}
