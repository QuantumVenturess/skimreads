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
                    // load new note image
                    var noteImage = $('#note_' + results.note_pk + ' .noteUserImage img');
                    noteImage.attr('src', noteImage.attr('data-original'));
                    // load new note form image
                    var noteFormImage = $('#noteForm img');
                    noteFormImage.attr('src', noteFormImage.attr('data-original'));
                    // load new comment form image
                    var commentFormImage = $('#commentForm_' + results.note_pk + ' img');
                    commentFormImage.attr('src', commentFormImage.attr('data-original'));
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