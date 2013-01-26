$(document).ready(function() {
    // Ajax voting note
    $('.noteVote form').live('submit', function() {
        var note = $(this).closest('.note');
        var id = note.attr('id').split('_')[1];
        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            success: function(results) {
                $('#note_' + results.pk + ' .noteVote').html(results.vote_form);
                var votes = parseInt($('#note_' + results.pk + ' .noteVotes').text());
                moveNote(id, results.pk, votes);
                $('.bulletNotes').html(results.bullet_notes);
            }
        })
        return false;
    })
    // Ajax voting reading
    $(document).on('submit', '.readingVote form', function() {
        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'),
            url:  $(this).attr('action'),
            success: function(results) {
                $('#reading_' + results.pk + ' .readingVote').html(results.vote_reading_form);
            }
        })
        return false;
    })
})

function moveNote(id, pk, votes) {
    var note = $('#note_' + id).closest('.note');
    var id = note.attr('id').split('_')[1];
    // Note below
    var next = note.next('.note');
    if (next.length > 0) {
        var nextId = next.attr('id').split('_')[1];
        var nextVotes = parseInt($('#note_' + nextId + ' .noteVotes').text());
        if (votes < nextVotes) {
            $('#note_' + pk).insertAfter(next)
            moveNote(id, pk, votes);
        }
    }
    // Note above
    var prev = note.prev('.note');
    if (prev.length > 0) {
        var prevId = prev.attr('id').split('_')[1];
        var prevVotes = parseInt($('#note_' + prevId + ' .noteVotes').text());
        if (votes > prevVotes) {
            $('#note_' + pk).insertBefore(prev)
            moveNote(id, pk, votes);
        }
    }
}