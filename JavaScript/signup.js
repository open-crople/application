    <!--아이디 중복 확인-->
    $(document).ready(function () {
        $("#button-duplicate").click(function () {
            var user_id = $("input[name='id']").val();

            $.ajax({
                type: "POST",
                url: "/check_duplicate_id",
                data: { id: user_id },
                success: function (response) {
                    if (response.status === 'duplicate') {
                        alert("이미 사용 중인 아이디입니다.");
                    } else {
                        alert("사용 가능한 아이디입니다.");
                    }
                }
            });
        });
    });
    
          <!--비밀번호를 *으로 숨기거나, 숫자로 표시하도록 하는 함수-->
        function togglePasswordVisibility(id) {
            var passwordField = document.getElementById(id);
            var eyeIcons = document.querySelectorAll('.eyeblock'+id);
            
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
