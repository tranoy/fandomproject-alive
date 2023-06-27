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