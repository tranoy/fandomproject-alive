'use strict';

(function ($) {

    /*------------------
        Preloader
    --------------------*/
    $(window).on('load', function () {
        $(".loader").fadeOut();
        $("#preloder").delay(200).fadeOut("slow");
    });


})(jQuery);


// 파일 업로드 avi mp4 제한
const form = document.getElementById('upload-form');
const fileInput = document.getElementById('video_file');
form.addEventListener('submit', function (event) {
    const fileName = fileInput.value;
    const allowedExtensions = /(\.mp4|\.avi)$/i;

    if (!allowedExtensions.exec(fileName)) {
        event.preventDefault(); // Prevent form submission

        const confirmUpload = confirm('Only MP4 and AVI files are allowed.');

        if (!confirmUpload) {
            return;
        }
    }
});


// 챌린지 START 페이지 로그인 된 사용자만 입장 제한
let entranceElements = document.getElementsByClassName('entrance_1');

for (let i = 0; i < entranceElements.length; i++) {
  entranceElements[i].addEventListener('click', function(event) {
    let sessionData = document.getElementById('check').textContent;
    console.log(sessionData);
    if (sessionData == '') {
      event.preventDefault();
      alert("로그인 후 사용하세요");
      window.location.href = '/login';
    }
  });
}


// 참고 영상 클릭 이벤트 추가
$('#ref-video').click(function (){
  var rowVideo = $('#row-video');
  if (rowVideo.css('opacity')==='0'){
    $(rowVideo).css({
      position: 'static',
      opacity: 1,
      visibility: 'visible',
      transition: 'visibility 0s, opacity 0.5s ease'
    });
  }
  else {
    $(rowVideo).css({
    visibility: 'hidden',
    position: 'absolute',
    opacity: 0,
  });
  }
});