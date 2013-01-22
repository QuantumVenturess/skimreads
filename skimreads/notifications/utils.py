def notify(comment=None, follow=None, note=None, 
            tie=None, reply=None, vote=None):
    """Create a notification for a user from current user."""
    # If a comment was created, notify the comment's note's user
    if comment:
        # If the comment's user is not the same as the note's user
        if comment.user != comment.note.user:
            comment.note.user.notification_set.create(comment=comment)
        # If the comment's user is not the same as the reading's user
        if comment.user != comment.note.reading.user:
            # If the note's user is not the same as the reading's user
            if comment.note.user != comment.note.reading.user:
                comment.note.reading.user.notification_set.create(
                    comment=comment)
    # If a current user follows another user, notify other user
    elif follow:
        # If the user is not following themselves
        if follow.followed != follow.follower:
            follow.followed.notification_set.create(follow=follow)
    # If a note as added to a reading
    elif note:
        # If the user who made the note doesn't own the reading
        if note.user != note.reading.user:
            note.reading.user.notification_set.create(note=note)
    # If a reply was made to a comment
    elif reply:
        # If the user who made the reply doesn't own the comment
        if reply.user != reply.comment.user:
            reply.comment.user.notification_set.create(reply=reply)
        # If the reply's user is not the same as the note's user
        if reply.user != reply.comment.note.user:
            # If the comment's user is not the same as the note's user
            if reply.comment.user != reply.comment.note.user:
                reply.comment.note.user.notification_set.create(reply=reply)
        # If the reply's user is not the same as the reading's user
        if reply.user != reply.comment.note.reading.user:
            # If the comment's user is not the same as the reading's user
            if reply.comment.user != reply.comment.note.reading.user:
                # If the note's user is not the same as the reading's user
                if reply.comment.note.user != reply.comment.note.reading.user:
                    reply.comment.note.reading.user.notification_set.create(
                        reply=reply)
    # If a tag was tied to a reading
    elif tie:
        # If the tie's user is not the reading's user
        if tie.user != tie.reading.user:
            tie.reading.user.notification_set.create(tie=tie)
    # If a user voted on a note
    elif vote:
        # If the vote's user is not the note's user
        if vote.user != vote.note.user:
            vote.note.user.notification_set.create(vote=vote)
        # If the vote's user is not the reading's user
        if vote.user != vote.note.reading.user:
            # If note's user is not the reading's user
            if vote.note.user != vote.note.reading.user:
                vote.note.reading.user.notification_set.create(vote=vote)