$(document).ready(function() {
    // Ajax follow form, follower, and following count
    $('.followForm form').live('submit', function() {
        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            success: function(results) {
                // If user is following a tag
                if (isNaN(results.user_id)) {
                    var pk = results.tag_pk;
                    // update topic follow form on topic page
                    $('#followForm_' + pk).html(results.tagfollow_form);
                    $('.tagfollowersCount').text(results.tagfollowers_count);
                    $('.topicCount').text(results.topic_count);
                    // update all tie follow forms
                    $('.tieFollowForm_' + pk).html(results.tiefollow_form);
                }
                // If user is following another user
                else {
                    var id = results.user_id;
                    $('#followForm_' + id).html(results.follow_form);
                    if (results.change_count > 0) {
                        $('.followersCount').text(results.followers_count);
                        $('.followingCount').text(results.following_count);
                    }
                }
            }
        })
        return false;
    })
    // Change following button to unfollow
    $('body').on('mouseenter', '.following, .unfollow', function() {
        var id = $(this).attr('id').split('_')[1]
        $('#following_' + id).hide();
        $('#unfollow_' + id).show();
    }).on('mouseleave', '.following, .unfollow', function() {
        var id = $(this).attr('id').split('_')[1]
        $('#following_' + id).show();
        $('#unfollow_' + id).hide();
    })
    // ajax topic follow form from the tag ties of a reading
    $(document).on('submit', '.tieFollowForm form', function() {
        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            success: function(results) {
                var pk = results.tag_pk;
                // update topic follow form on topic page
                $('#followForm_' + pk).html(results.tagfollow_form);
                $('.tagfollowersCount').text(results.tagfollowers_count);
                $('.topicCount').text(results.topic_count);
                // update all tie follow forms
                $('.tieFollowForm_' + pk).html(results.tiefollow_form);
            }
        })
        return false;
    })
    // when hovering over a tie tag, show the follow/unfollow button
    $(document).on('mouseover', '.tie', function() {
        var id = $(this).attr('id');
        $('.tieFollowForm').hide();
        $('#' + id + ' .tieFollowForm').show();
        return false;
    })
    // when hovering outside of the tie tag, hide follow/unfollow button
    $(document).on('mouseover', 'body', function() {
        $('.tieFollowForm').hide();
    })
})