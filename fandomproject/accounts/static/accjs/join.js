// clickmotion javascript
let id = $('#id');
let nick = $('#nick');
let pw1 = $('#pw1');
let pw2 = $('#pw2');
let btn = $('#join_btn');
let email = $('#email');
    $(btn).on('click', function() {
        if($(id).val() == "") {
            $(id).next('label').addClass('warning');
            setTimeout(function()  {
                $('label').removeClass('warning');
            }, 1500);
        };
        if($(nick).val() == "") {
            $(nick).next('label').addClass('warning');
            setTimeout(function()  {
                $('label').removeClass('warning');
            }, 1500);
        };
        if($(email).val() == "") {
            $(email).next('label').addClass('warning');
            setTimeout(function()  {
                $('label').removeClass('warning');
            }, 1500);
        };
        if($(pw1).val() == "") {
            $(pw1).next('label').addClass('warning');
            setTimeout(function()  {
                $('label').removeClass('warning');
            }, 1500);
        };
        if($(pw2).val() == "") {
            $(pw2).next('label').addClass('warning');
            setTimeout(function()  {
                $('label').removeClass('warning');
            }, 1500);
        };
    });




let checkBtn = $('#join-id-check');

// join버튼 조건에 bool값 추가
// id check 버튼을 먼저 누르고 유효성 맞아야지 true로 바껴서 join이 될 수 있도록

let checkBool = false;
$(checkBtn).on('click', function() {
    let nickname = $('#nick').val();
    let idRegex = /^[a-z0-9]{6,}$/;

    if (nickname === ''){
        return
    };
    if (!idRegex.test(nickname)) {
        $('#nick').next('label').addClass('warning').text('영소문자와 숫자로 구성된 6글자 이상으로 작성해주세요');
        checkBool = false
    }
    else{
        $('#nick').next('label').removeClass('warning').text('ID');
        $.ajax({
            url : "/login/join",
            data : {
                nickname : nickname
            },
            method : "POST",
            success : function (id_data) {
                if (id_data.id_exists) {
                // 이메일 이미 존재하는 경우 오류 메시지 표시
                $('#nick').next('label').addClass('warning').text('이미 존재하는 아이디 입니다.');
                }else{
                $('#nick').next('label').removeClass('warning').text('ID');
                checkBool = true
                };
            },
            error : function (request, status, error){
                console.log("에러");
            },
            complete : function () {
                console.log("완료");
                
            },
        });
    };
});


// 비밀번호 형식 지정
let passwordCheck = false;
$(document).ready(function(){
    let reg = /^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$/;
    $('#pw1').on('blur',function(){
        let password1 = $('#pw1').val();
        if(false === reg.test(password1)){
            $('#pw1').next('label').addClass('warning').text('비밀번호는 8자리 이상, 숫자/대문자/소문자/특수문자를 모두 포함');
            passwordCheck = false
        }
        if (password1 === ''){
            $('#pw1').next('label').removeClass('warning').text('PASSWORD');
        }
        else if(reg.test(password1)){
            $('#pw1').next('label').removeClass('warning').text('PASSWORD');
            passwordCheck = true
        };
    });
});


$(document).ready(function() {
  // 비밀번호 일치 여부 확인
  $('#pw2').on('blur', function() {
    let password1 = $('#pw1').val();
    let password2 = $(this).val();

    if (password1 !== password2) {
      // 비밀번호가 일치하지 않는 경우 오류 메시지 표시
      $('#pw2').next('label').addClass('warning').text('Passwords do not match');
    } else {
      // 비밀번호가 일치하는 경우 오류 메시지 제거
      $('#pw2').next('label').removeClass('warning').text('PASSWORD CHECK');

    };
  });
});


// post 방식 비동기 처리 ==> account views.py class
$('#join_btn').click(function () {

    let username = $('#id').val();
    let nickname = $('#nick').val();
    let password1 = $('#pw1').val();
    let password2 = $('#pw2').val();
    let email = $('#email').val();

    let emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)){
        $('#email').next('label').addClass('warning').text('유효한 이메일 형식으로 작성해주세요');
        emailCheck = false;
    }else{
        $('#email').next('label').removeClass('warning').text('EMAIL');
        emailCheck = true;
    }
    if (username && nickname && password1 && password2 && email && checkBool && emailCheck && passwordCheck) {

    // ajax 통신
    $.ajax({
        url : "/login/join",
        data : {
            username : username,
            nickname : nickname,
            password1 : password1,
            password2 : password2,
            email : email, 
        },
        method : "POST",
        // 회원가입 성공시 로그인 페이지로
            success : function (data) {
                if (data.exists) {
                // 이메일 이미 존재하는 경우 오류 메시지 표시
                $('#email').next('label').addClass('warning').text('이미 존재하는 이메일 입니다');
                } else {
                // 이메일 존재하지 않는 경우 오류 메시지 제거
                $('#email').next('label').removeClass('warning').text('ID');
                console.log("성공");
                alert("회원가입 성공했습니다. 로그인 해주세요.");
                location.replace("/login");
                }   
            },
            error : function (request, status, error){
                console.log("에러");
            },
            complete : function () {
                console.log("완료");
            },
        });
    };
});
