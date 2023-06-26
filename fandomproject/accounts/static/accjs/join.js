
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
        }
        if($(nick).val() == "") {
            $(nick).next('label').addClass('warning');
            setTimeout(function()  {
                $('label').removeClass('warning');
            }, 1500);
        }
        if($(email).val() == "") {
            $(email).next('label').addClass('warning');
            setTimeout(function()  {
                $('label').removeClass('warning');
            }, 1500);
        }
        if($(pw1).val() == "") {
            $(pw1).next('label').addClass('warning');
            setTimeout(function()  {
                $('label').removeClass('warning');
            }, 1500);
        }
        if($(pw2).val() == "") {
            $(pw2).next('label').addClass('warning');
            setTimeout(function()  {
                $('label').removeClass('warning');
            }, 1500);
        }
    });



// $(document).ready(function() {
//     // 아이디 중복 검사
//     $('#id').on('blur', function() {
//         var username = $(this).val();
      
//         $.ajax({
//         url: '/login/join',  // 아이디 중복 검사를 처리하는 URL
//         method: 'POST',
//         data: {
//             username: username
//         },
//         success: function(response) {
//             if (response.exists) {
//             // 아이디가 이미 존재하는 경우 오류 메시지 표시
//             $('#id').next('label').addClass('warning').text('This ID is already taken');
//             } else {
//             // 아이디가 존재하지 않는 경우 오류 메시지 제거
//             $('#id').next('label').removeClass('warning').text('ID');
//             }
//         },
//     });
//     });
// });
// $(document).ready(function() {
//     // 아이디 중복 검사
//     $('#nick').on('blur', function() {
//       let nickname = $(this).val();
//       let username = $('#username').val();  // username 필드 값 가져오기
//       let password1 = $('#pw1').val();  // password1 필드 값 가져오기
//       let password2 = $('#pw2').val();  // password2 필드 값 가져오기
//       let email = $('#email').val();  // email 필드 값 가져오기
  
//       // Ajax 요청
//       $.ajax({
//         url: '/login/join',  // 서버의 URL 주소
//         method: 'POST',
//         headers: { 'X-CSRFToken': '{{ csrf_token }}' },
//         data: { nickname: nickname,
//             username: username,
//             password1: password1,
//             password2: password2,
//             email: email },  // 전송할 데이터
  
//         success: function(response) {
//           if (response.exists) {
//             // 아이디가 이미 존재하는 경우 오류 메시지 표시
//             $('#nick').next('label').addClass('warning').text('This ID is already taken');
//           } else {
//             // 아이디가 존재하지 않는 경우 오류 메시지 제거
//             $('#nick').next('label').removeClass('warning').text('ID');
//           }
//         },
  
//         error: function(request, status, error) {
//           console.log('An error occurred during username check:', error);
//         }
//       });
//     });
//   });


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
    }
  })
})

// post 방식 비동기 처리 ==> account views.py class
$('#join_btn').click(function () {

    let username = $('#id').val();
    let nickname = $('#nick').val();
    let password1 = $('#pw1').val();
    let password2 = $('#pw2').val();
    let email = $('#email').val();
    if (username && nickname && password1 && password2 && email) {
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
            // 아이디가 이미 존재하는 경우 오류 메시지 표시
            $('#email').next('label').addClass('warning').text('This EMAIL is already taken');
            } else {
            // 아이디가 존재하지 않는 경우 오류 메시지 제거
            $('#email').next('label').removeClass('warning').text('ID');
            console.log("성공");
            alert("회원가입 성공했습니다. 로그인 해주세요.")
            location.replace("/login");
            }
        },
        error : function (request, status, error){
            console.log("에러");
        },
        complete : function () {
            console.log("완료");
        },
    })
}
})
