$(document).ready(function() {
    // Login menu
    var login = $('.login');
    var loginMenu = $('#loginMenu');
    login.live('mouseover', function() {
        $(this).addClass('menuShow');
        loginMenu.show();
        var email = $('#loginEmail');
        var password = $('#loginPassword');
        if (email.val() == '') {
            email.focus();
        }
        else if (password.val() == '') {
            password.focus();
        }
        return false;
    })
    loginMenu.live('mouseover', function() {
        return false;
    })
    $(document).live('mouseover', function() {
        /*
        var email = $('#loginEmail');
        var password = $('#loginPassword');
        if (email.val() == '' && password.val() == '') {
            login.removeClass('menuShow');
            loginMenu.hide();
        }
        */
        login.removeClass('menuShow');
        loginMenu.hide();
    })
    $('#loginMenu form').live('submit', function() {
        var email = $('#loginEmail');
        var password = $('#loginPassword');
        if (email.val() == '') {
            email.focus();
            return false;
        }
        else if (password.val() == '') {
            password.focus();
            return false;
        }
    })
    // Account menu
    $('.account').live('mouseover', function() {
        $(this).addClass('menuShow');
        $('#menu').show();
        return false;
    })
    $('#menu').live('mouseover', function() {
        return false;
    })
    $(document).live('mouseover', function() {
        $('.account').removeClass('menuShow');
        $('#menu').hide();
    })
})