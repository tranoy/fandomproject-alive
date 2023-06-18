let id = $('#id');
        let pw = $('#pw');
        let btn = $('#login_btn');

        $(btn).on('click', function() {
            if($(id).val() == "") {
                $(id).next('label').addClass('warning');
                setTimeout(function()  {
                    $('label').removeClass('warning');
                }, 1500);
            }
            else if($(pw).val() == "") {
                $(pw).next('label').addClass('warning');
                setTimeout(function()  {
                    $('label').removeClass('warning');
                }, 1500);
            }
        });


$('#login_btn').click(function () {

    let username = $('#id').val();
    let password = $('#pw').val();
    // ajax 통신
    $.ajax({
        url : "/login/join",
        data : {
            username : username,
            password : password,
        },
        method : "POST",
        // 회원가입 성공시 로그인 페이지로
        success : function (data) {
            console.log("성공");
            alert("로그인 성공")
            location.replace("/");
        },
        error : function (request, status, error){
            console.log("에러");
        },
        complete : function () {
            console.log("완료");
        },
    })
})