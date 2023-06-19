
// clickmotion javascript
let id = $('#id');
        let pw1 = $('#pw1');
        let pw2 = $('#pw2');
        let btn = $('#join_btn');
        $(btn).on('click', function() {
            if($(id).val() == "") {
                $(id).next('label').addClass('warning');
                setTimeout(function()  {
                    $('label').removeClass('warning');
                }, 1500);
            }
            else if($(pw1).val() == "") {
                $(pw1).next('label').addClass('warning');
                setTimeout(function()  {
                    $('label').removeClass('warning');
                }, 1500);
            }
            else if($(pw2).val() == "") {
                $(pw2).next('label').addClass('warning');
                setTimeout(function()  {
                    $('label').removeClass('warning');
                }, 1500);
            }
        });

$('#join_btn').click(function () {

    let username = $('#id').val();
    let password = $('#pw1').val();
    let password_2 = $('#pw2').val();
    let email = $('#email').val();

    console.log(username,password,email)
    
    // ajax 통신
    $.ajax({
        url : "/login/join",
        data : {
            username : username,
            password : password,
            password_2 : password_2,
            email : email, 
        },
        method : "POST",
        // 회원가입 성공시 로그인 페이지로
        success : function (data) {
            console.log("성공");
            alert("회원가입 성공했습니다. 로그인 해주세요.")
            location.replace("/login");
        },
        error : function (request, status, error){
            console.log("에러");
        },
        complete : function () {
            console.log("완료");
        },
    })
})
