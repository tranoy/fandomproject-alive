

// 모달 창 요소 가져오기
var modal = document.getElementById("upload-modal");
var submitBtn = document.getElementById("submit-btn")



// 업로드 버튼 클릭 시 모달 창 열기
var uploadButton = document.getElementById("upload-button");
uploadButton.addEventListener("click", function() {
  modal.style.display = "flex";
});

// 모달 창 닫기 버튼 클릭 시 모달 창 닫기
var closeButton = document.getElementsByClassName("close")[0];
closeButton.addEventListener("click", function() {
  modal.style.display = "none";
});

// 모달 창 외부 클릭 시 모달 창 닫기
window.addEventListener("click", function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
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

var videoFile = document.getElementById("video-file");
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





var selectVideo = document.getElementById("video-file");
selectVideo.addEventListener("change", function(){
    const file = selectVideo.files[0];
    const videourl = URL.createObjectURL(file);
    console.log("heelo")
    console.log(file,videourl)
})

// 업로드 폼 제출 시 처리
var uploadForm = document.getElementById("upload-form");
uploadForm.addEventListener("submit", function(event) {
  event.preventDefault();

  // 비디오 업로드 처리 로직 추가
  var videoTitle = document.getElementById("video-title").value;
  var videoFile = document.getElementById("video-file");
  
  console.log("제목:", videoTitle);
  console.log("파일명:", videoFile);
 
  
  // 업로드 완료 메시지 또는 다른 처리 로직 추가
  // 여기서는 간단히 콘솔에 업로드 완료 메시지를 출력하는 예시를 보여줍니다.
  console.log("비디오 업로드가 완료되었습니다.");

  // 모달 창 닫기
  modal.style.display = "none";
});
