$(document).ready(function() {
    // Toggle show and hide replies
    $('.commentDateTime a').live('click', function() {
        var id = $(this).attr('id').split('_')[1];
        $('#replies_' + id).toggle();
        $('#replyForm_' + id + ' textarea#id_content').focus();
        return false;
    })
    // Ajax reply new
    $('.replyForm form').live('submit', function() {
        var id = $(this).attr('id').split('_')[1];
        var content = $('#replyForm_' + id + ' textarea#id_content');
        if (content.val().length > 0) {
            $.ajax({
                data: $(this).serialize(),
                type: $(this).attr('method'),
                url: $(this).attr('action'),
                success: function(results) {
                    $('#replies_' + results.comment_pk + ' .replies').append(results.reply);
                    $('#replyCount_' + results.comment_pk).text(results.reply_count);
                    $('#replyFormContainer_' + results.comment_pk).html(results.reply_form);
                    $('textarea').autoResize();
                    // load new reply image
                    var replyImage = $('#reply_' + results.reply_pk + ' .replyUserImage img');
                    replyImage.attr('src', replyImage.attr('data-original'));
                    // load new reply form image
                    var replyFormImage = $('#replyForm_' + results.comment_pk + ' img');
                    replyFormImage.attr('src', replyFormImage.attr('data-original'));
                }
            })
        }
        else {
            content.focus();
        }
        return false;
    })
    // Textarea enter submit
    $('.replyForm textarea').live('keydown', function(event) {
        var form = $(this).closest('form');
        if (event.keyCode == 13 && !event.shiftKey) {
            form.submit();
            return false;
        }
    })
    // Ajax reply delete
    $('.replyDelete form').live('submit', function() {
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
                            $('#reply_' + results.comment_pk).remove()
                            $('#replyCount_' + results.comment_pk).text(results.reply_count);
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