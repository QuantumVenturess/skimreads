$(document).ready(function() {
    // Ajax note new
    $('#noteForm form').live('submit', function() {
        var content = $('#noteForm textarea#id_content');
        if (content.val().length > 0) {
            $.ajax({
                data: $(this).serialize(),
                type: $(this).attr('method'),
                url: $(this).attr('action'),
                success: function(results) {
                    $('.bulletNotes').html(results.bullet_notes);
                    $('.notes').append(results.note);
                    $('#noteForm').html(results.note_form);
                    $('textarea').autoResize();
                }
            })
        }
        else {
            content.focus();
        }
        return false;
    })
    // Ajax note delete
    $('.noteDelete form').live('submit', function() {
        var form = $(this);
        $('.confirmDelete').dialog({
            resizable: false,
            height: 100,
            buttons: {
                'Delete': function() {
                    $.ajax({
                        data: form.serialize(),
                        type: form.attr('method'),
                        url: form.attr('action'),
                        success: function(results) {
                            if (results.note_count > 1) {
                                $('.bulletNotes').html(results.bullet_notes);
                                $('#note_' + results.pk).remove();
                            }
                            else {
                                alert('You cannot delete the only note')
                            }
                        }
                    })
                    $('.confirmDelete').dialog('close');
                },
                Cancel: function() {
                    $(this).dialog('close');
                }
            }
        })
        return false;
    })
})