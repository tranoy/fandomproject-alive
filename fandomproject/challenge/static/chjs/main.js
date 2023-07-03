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
		Navigation
	--------------------*/

})(jQuery);


  


let entranceElements = document.getElementsByClassName('entrance_1');

for (let i = 0; i < entranceElements.length; i++) {
  entranceElements[i].addEventListener('click', function(event) {
    console.log("발동1");
    let sessionData = document.getElementById('check').textContent;
    console.log(sessionData);
    if (sessionData == '') {
      event.preventDefault();
      console.log("발동2");
      alert("로그인 후 사용하세요");
      window.location.href = '/login';
    }
  });
}


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