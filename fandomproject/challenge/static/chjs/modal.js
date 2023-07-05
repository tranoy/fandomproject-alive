// 모달 창 요소 가져오기
var modal = document.getElementById("upload-modal");
var submitBtn = document.getElementById("submit-btn");

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

uploadContentForm = document.getElementById("upload-content-form");

// 업로드 폼 제출 시 처리
var uploadForm = document.getElementById("upload-form");
uploadForm.addEventListener("submit", function(event) {

  uploadContentForm.style.display ="block";

});
