$(document).ready(function() {
    // Notification forward to reading detail show
    var focus = $('.focus');
    $('.show').show();
    if (focus.length > 0) {
        var focusTop = focus.offset().top;
        $('html, body').animate({ scrollTop: focusTop - 50 }, 0);
        focus.delay(5000).queue(function() {
            $(this).removeClass('focus');
        })
    }
})