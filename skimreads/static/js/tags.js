$(document).ready(function() {
    // Adding a tag
    $(document).on('submit', '.tagForm form', function() {
        var bannedWords = /ass|bitch|cock|cunt|dick|fag|fuck|gay|queer|shit|pussy|tit|vagina/
        var form = $('.tagForm form');
        var regex = /^[A-Za-z]+$/
        var value = $('#id_tag_name').val();
        if (value.match(regex) && !value.match(bannedWords)) {
            $.ajax({
                data: form.serialize(),
                type: form.attr('method'),
                url: form.attr('action'),
                success: function(results) {
                    $('.tagForm form').remove();
                    $('.tags').html(results.ties)
                }
            })
        }
        else if (!value.match(regex)) {
            $('#id_tag_name').focus();
            alert('Use only letters with no spaces')
        }
        else if (value.match(bannedWords)) {
            $('#id_tag_name').val('');
            alert('Please use appropriate words');
        }
        return false;
    })
    // pressing enter on an autocomplete option will submit the tie form
    $('.tagForm input').live('keyup', function(e) {
        if (e.keyCode == 13) {
            var bannedWords = /ass|bitch|cock|cunt|dick|fag|fuck|gay|queer|shit|pussy|tit|vagina/
            var form = $('.tagForm form');
            var regex = /^[A-Za-z]+$/
            var value = $('#id_tag_name').val();
            if (value.match(regex) && !value.match(bannedWords)) {
                $.ajax({
                    data: form.serialize(),
                    type: form.attr('method'),
                    url: form.attr('action'),
                    success: function(results) {
                        $('.tagForm form').remove();
                        $('.tags').html(results.ties)
                    }
                })
            }
            else if (!value.match(regex)) {
                $('#id_tag_name').focus();
                alert('Use only letters with no spaces')
            }
            else if (value.match(bannedWords)) {
                $('#id_tag_name').val('');
                alert('Please use appropriate words');
            }
            return false;
        }
    })
    // Clicking on an autocomplete option will submit the tie form
    $('.ui-autocomplete .ui-menu-item a').live('click', function() {
        var form = $('.tagForm form');
        if (form.length > 0) {
            $('.tagForm .field input').val($(this).text());
            $.ajax({
                data: form.serialize(),
                type: form.attr('method'),
                url: form.attr('action'),
                success: function(results) {
                    $('.tagForm form').remove();
                    $('.tags').html(results.ties)
                }
            })
        }
    })
    // Deleting a tag
    $('.tie form').live('submit', function() {
        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            success: function(results) {
                $('.tagForm').html(results.tag_form);
                $('#tie_' + results.tie_id).remove();
            }
        })
        return false;
    })
})