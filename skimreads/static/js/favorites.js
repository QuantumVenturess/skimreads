$(document).ready(function() {
    // Saving or unsaving a favorite reading
    $('.favoriteForm form').live('submit', function() {
        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            success: function(results) {
                var pk = results.pk;
                $('.favoriteCount').text(results.favorite_count);
                $('#favoriteForm_' + pk).html(results.favorite_form);
            }
        })
        return false;
    })
})