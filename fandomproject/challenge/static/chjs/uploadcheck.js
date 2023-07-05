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