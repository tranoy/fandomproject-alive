/*  ---------------------------------------------------
  Template Name: DJoz
  Description:  DJoz Music HTML Template
  Author: Colorlib
  Author URI: https://colorlib.com
  Version: 1.0
  Created: Colorlib
---------------------------------------------------------  */

'use strict';

(function ($) {

    /*------------------
        Preloader
    --------------------*/
    $(window).on('load', function () {
        $(".loader").fadeOut();
        $("#preloder").delay(200).fadeOut("slow");
    });

    /*------------------
        Background Set
    --------------------*/
    $('.set-bg').each(function () {
        var bg = $(this).data('setbg');
        $(this).css('background-image', 'url(' + bg + ')');
    });

    /*------------------
		Navigation
	--------------------*/
    $(".mobile-menu").slicknav({
        prependTo: '#mobile-menu-wrap',
        allowParentLinks: true
    });
    
    /*--------------------------
        Event Slider
    ----------------------------*/
    $(".event__slider").owlCarousel({
        loop: true,
        margin: 0,
        items: 3,
        dots: false,
        nav: true,
        navText: ["<i class='fa fa-angle-left'></i>","<i class='fa fa-angle-right'></i>"],
        smartSpeed: 1200,
        autoHeight: false,
        autoplay: true,
        responsive: {
            992: {
                items: 3,
            },
            768: {
                items: 2,
            },
            0: {
                items: 1,
            },
        }
    });
    
    /*--------------------------
        Videos Slider
    ----------------------------*/
    $(".videos__slider").owlCarousel({
        loop: true,
        margin: 0,
        items: 4,
        dots: false,
        nav: true,
        navText: ["<i class='fa fa-angle-left'></i>","<i class='fa fa-angle-right'></i>"],
        smartSpeed: 1200,
        autoHeight: false,
        autoplay: true,
        responsive: {
            992: {
                items: 4,
            },
            768: {
                items: 3,
            },
            576: {
                items: 2,
            },
            0: {
                items: 1,
            }
        }
    });

    /*------------------
		Magnific
	--------------------*/
    $('.video-popup').magnificPopup({
        type: 'iframe'
    });

    /*------------------
        CountDown
    --------------------*/
    // For demo preview
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = today.getFullYear();

    if(mm == 12) {
        mm = '01';
        yyyy = yyyy + 1;
    } else {
        mm = parseInt(mm) + 1;
        mm = String(mm).padStart(2, '0');
    }
    var timerdate = mm + '/' + dd + '/' + yyyy;
    // For demo preview end
    

    // Use this for real timer date
    /* var timerdate = "2020/01/01"; */

	$("#countdown-time").countdown(timerdate, function(event) {
        $(this).html(event.strftime("<div class='countdown__item'><span>%D</span> <p>Days</p> </div>" + "<div class='countdown__item'><span>%H</span> <p>Hours</p> </div>" + "<div class='countdown__item'><span>%M</span> <p>Minutes</p> </div>" + "<div class='countdown__item'><span>%S</span> <p>Seconds</p> </div>"));
    });

    /*------------------
		Barfiller
	--------------------*/
    $('#bar1').barfiller({
        barColor: "#ffffff",
    });

    $('#bar2').barfiller({
        barColor: "#ffffff",
    });

    $('#bar3').barfiller({
        barColor: "#ffffff",
    });

    /*-------------------
		Nice Scroll
	--------------------- */
    $(".nice-scroll").niceScroll({
        cursorcolor: "#111111",
        cursorwidth: "5px",
        background: "#e1e1e1",
        cursorborder: "",
        autohidemode: false,
        horizrailenabled: false
    });

})(jQuery);


function handleDrop(event) {
    event.preventDefault();
    var file = event.dataTransfer.files[0];
    var input = document.getElementById("chooseImage");
    input.files = event.dataTransfer.files;
    handleFiles(input.files);
  }

  function handleDragOver(event) {
    event.preventDefault();
    var file = event.dataTransfer.items[0].getAsFile();
    var input = document.getElementById("chooseImage");
    input.files = event.dataTransfer.files;
    handleFiles(input.files);
  }

  function handleFiles(files) {
    const imagePreviewContainer = document.getElementById(
      "image-preview-container"
    );
    const previewImage = document.getElementById("previewImage");
    const dragMessage = document.querySelector("#drop-file .drag_message"); // 추가

    if (files.length === 0) {
      imagePreviewContainer.innerHTML = ""; // 이미지 미리보기 컨테이너를 비웁니다.
      dragMessage.style.display = "block"; // 이미지가 없을 때는 메시지를 보이도록 설정
      return;
    }

    const file = files[0];
    const reader = new FileReader();

    reader.onload = function (event) {
      const imageUrl = event.target.result;
      previewImage.src = imageUrl;
      dragMessage.style.display = "none"; // 이미지가 업로드되면 메시지를 숨김

      // 선택한 이미지를 이미지 미리보기 컨테이너 안에도 표시할 수 있습니다. (선택사항)
      const imagePreview = document.createElement("img");
      imagePreview.src = imageUrl;
      imagePreviewContainer.innerHTML = ""; // 추가하기 전에 컨테이너를 비웁니다.
      imagePreviewContainer.appendChild(imagePreview);
    };

    reader.readAsDataURL(file);
  }

  function handleFile(file) {
    var reader = new FileReader();
    reader.onload = function (event) {
      var img = document.getElementById("previewImage");
      img.src = event.target.result;
    };
    reader.readAsDataURL(file);
  }

  function uploadImage(event) {
    event.preventDefault();

    const fileInput = document.getElementById("chooseImage");
    const file = fileInput.files[0];

    if (!file) {
      return;
    }

    const formData = new FormData();
    formData.append("image", file);
    formData.append(
      "style",
      document.querySelector("select[name='style']").value
    );

    fetch("{% url 'making:transform' %}", {
      method: "POST",
      body: formData,
      headers: {
        "X-CSRFToken": document.querySelector(
          "[name='csrfmiddlewaretoken']"
        ).value,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        // 이미지 저장 및 출력 처리
        sessionStorage.setItem("transformedImage", data.transformed_image);
        window.location.href = "{% url 'making:display' %}";
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }

  const createAlbumArtButton = document.getElementById(
    "create-album-art-button"
  );
  createAlbumArtButton.addEventListener("click", uploadImage);

  // 페이지 로드 시 이미지 미리보기 처리
  window.addEventListener("DOMContentLoaded", function () {
    var fileInput = document.getElementById("chooseImage");
    fileInput.addEventListener("change", function () {
      handleFiles(fileInput.files);
    });
  });