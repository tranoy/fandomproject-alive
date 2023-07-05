let id = $('#nick');
let pw = $('#pw');
let btn = $('#login_btn');

// login button click event
$(btn).on('click', function() {
    if($(id).val() == "") {
        $(id).next('label').addClass('warning');
        setTimeout(function()  {
            $('label').removeClass('warning');
        }, 1500);
    }
    else if($(pw).val() == "") {
        $(pw).next('label').addClass('warning');
        setTimeout(function()  {
            $('label').removeClass('warning');
        }, 1500);
    };
});
