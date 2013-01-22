$(document).ready(function() {
    var signUpForm = $('#signUpForm');
    // Show sign up form
    $('.signUpPop').live('click keyup', function() {
        var left = $(this).offset().left;
        var top = $(this).offset().top;
        var height = signUpForm.height();
        var width = signUpForm.width();
        signUpForm.css('left', left - width);
        signUpForm.css('top', top - height);
        signUpForm.show();
        var name = $('#username');
        var nameVal = name.val();
        var email = $('#email');
        var emailVal = email.val();
        var pw = $('#password');
        var pwVal = pw.val();
        // If name blank
        if (nameVal.length == 0) {
            name.focus();
        }
        // If email blank
        else if (emailVal.length == 0) {
            email.focus();
        }
        // If password blank
        else if (pwVal.length == 0) {
            pw.focus();
        }
        return false;
    })
    // Clicking anywhere to hide sign up form
    signUpForm.live('click', function(event) {
        event.stopPropagation();
    })
    $(document).live('click', function() {
        signUpForm.hide();
    })
    // Submitting sign up form via ajax
    $('#signUpForm form').live('submit', function() {
        // Username
        var name = $('#username');
        var nameVal = name.val();
        if (nameVal.length == 0) {
            name.focus();
            return false;
        }
        else if (nameVal.length > 30) {
            alert('Name cannot be more than 30 characters')
            name.focus();
            return false;
        }
        else if (!nameVal.match(/^[-A-Za-z]{2,} [-A-Za-z]{2,}$/)) {
            alert('Please enter your full name')
            name.focus();
            return false;
        }
        // Email
        var email = $('#email');
        var emailVal = email.val();
        if (emailVal.length == 0) {
            email.focus();
            return false;
        }
        else if (!emailVal.match(/^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$/i)) {
            alert('Please enter in a valid email');
            email.focus();
            return false;
        }
        // Password
        var pw = $('#password');
        var pwVal = pw.val();
        if (pwVal.length == 0) {
            pw.focus();
            return false;
        }
        // Ajax
        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            success: function(results) {
                // If the user successfully signed up
                if (results.success == 'yes') {
                    // Update each comment & vote form
                    var comment_forms = results.comment_forms;
                    jQuery.each(comment_forms, function(pk, form) {
                        $('#commentFormContainer_' + pk).html(form);
                    })
                    // Insert favorite form
                    $('.favoriteForm').html(results.favorite_form);
                    // Update the header
                    $('header').html(results.header);
                    // Update the note form
                    $('#noteForm').html(results.note_form);
                    // Update each reply form
                    var reply_forms = results.reply_forms;
                    jQuery.each(reply_forms, function(pk, form) {
                        $('#replyFormContainer_' + pk).html(form);
                    })
                    // Update the tag form
                    $('.tagForm').html(results.tag_form);
                    // Update each vote form
                    var vote_forms = results.vote_forms;
                    jQuery.each(vote_forms, function(pk, form) {
                        $('#note_' + pk + ' .noteVote').html(form);
                    })
                    // Remove the sign up form
                    signUpForm.remove();
                }
                // If the user was not created
                else {
                    alert('Name and/or email is already registered')
                }
            }
        })
        return false;
    })
})