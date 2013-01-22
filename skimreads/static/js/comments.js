$(document).ready(function() {
    // Toggle show and hide comments
    $(document).on('click', '.note .noteDateTime a', function() {
        var id = $(this).attr('id').split('_')[1];
        $('#comments_' + id).toggle();
        $('#commentForm_' + id + ' textarea#id_content').focus();
        return false;
    })
    // Ajax comment new
    $(document).on('submit', '.commentForm form', function() {
        var id = $(this).attr('id').split('_')[1];
        var content = $('#commentForm_' + id + ' textarea#id_content');
        if (content.val().length > 0) {
            $.ajax({
                data: $(this).serialize(),
                type: $(this).attr('method'),
                url: $(this).attr('action'),
                success: function(results) {
                    $('#comments_' + results.pk + ' .comments').append(results.comment);
                    $('#commentCount_' + results.pk).text(results.comment_count);
                    $('#commentFormContainer_' + results.pk).html(results.comment_form);
                    $('textarea').autoResize();
                }
            })
        }
        else {
            content.focus();
        }
        return false;
    })
    // Textarea enter submit
    $(document).on('keydown', '.commentForm textarea', function(event) {
        var form = $(this).closest('form');
        if (event.keyCode == 13 && !event.shiftKey) {
            form.submit();
            return false;
        }
    })
    // Ajax comment delete
    $(document).on('submit', '.commentDelete form', function() {
        var confirm = $('.confirmDelete');
        var form = $(this);
        confirm.dialog({
            resizable: false,
            height: 100,
            buttons: {
                'Delete': function() {
                    $.ajax({
                        data: form.serialize(),
                        type: form.attr('method'),
                        url: form.attr('action'),
                        success: function(results) {
                            $('#comment_' + results.pk).remove();
                            $('#commentCount_' + results.note_pk).text(results.comment_count);
                        }
                    })
                    confirm.dialog('close');
                },
                Cancel: function() {
                    $(this).dialog('close');
                }
            }
        })
        return false;
    })
})