

// 모달 창 요소 가져오기
var modal = document.getElementById("upload-modal");
var submitBtn = document.getElementById("submit-btn");

// 스크롤바 없애기

// 업로드 버튼 클릭 시 모달 창 열기
// var uploadButton = document.getElementById("upload-button");
// uploadButton.addEventListener("click", function() {
//   modal.style.display = "flex";
//   overflow : this.hidden
// });
$("#video_file").on('change',function(){
  var fileName = $("#video_file").val();
  $(".upload-name").val(fileName);
});

$('#upload-button').click(function (){
  $('.modal-box').css({
    display : 'flex',
  });
  $(document.body).css({
    overflow : 'hidden',
  });
});

// 모달 창 닫기 버튼 클릭 시 모달 창 닫기
var closeButton = document.getElementsByClassName("close")[0];
closeButton.addEventListener("click", function() {
  modal.style.display = "none";
  document.body.style.overflow = "visible";
});

// 모달 창 외부 클릭 시 모달 창 닫기
window.addEventListener("click", function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
    document.body.style.overflow = "visible";
  }
});

var check1 = false
var check2 = false

var videoTitle = document.getElementById("video-title");
    videoTitle.addEventListener("change",function(){
        if (videoTitle.value != ''){
            check1 = true
        }
        else{
            check1 = false
        }
        console.log(check1)

    })

var videoFile = document.getElementById("video_file");
    videoFile.addEventListener("change",function(){
        if(videoFile.files.length > 0){
            check2 = true
        }
        else{
            check2 = false
        }
        console.log(check2)

    })

// if (check1 && check2){
//     submitBtn.disabled = false

// }

// else{
//     submitBtn.disabled = true
// }



uploadContentForm = document.getElementById("upload-content-form");

// 업로드 폼 제출 시 처리
var uploadForm = document.getElementById("upload-form");
uploadForm.addEventListener("submit", function(event) {
  event.preventDefault();

  uploadContentForm.style.display ="block";

});
