$(document).ready(function() {
    // to top button
    var top = $('.topButton');
    $('.toTop').live('click', function() {
        top.addClass('stopScroll');
        $('html, body').animate({ scrollTop: 0 }, 200, function() {
            top.removeClass('stopScroll');
        });
        return false;
    });
    $(window).scroll(function() {
        if ($(window).scrollTop() > $(window).height() * 1 && !top.hasClass('stopScroll')) {
            top.slideDown(100);
        }
        else {
            top.slideUp(100);
        }
    })
})