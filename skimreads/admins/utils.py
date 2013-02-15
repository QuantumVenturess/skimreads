from django.contrib.auth.models import User
from random import randint
from users.utils import add_rep

def admin_david_list():
    """Return users for david."""
    pks = [2, 17, 18, 19, 20]
    users = User.objects.filter(pk__in=pks).order_by('date_joined')
    return users

def admin_user_list():
    """Return the available users for an admin to select from
    when adding a new reading."""
    pks = range(1, 11) # list from 1 to 10
    users = User.objects.filter(pk__in=pks).order_by('date_joined')
    return users

def auto_vote(request, reading):
    notes = reading.note_set.all()
    users = first_ten_users()
    # create votes for first ten users
    for user in users:
        # vote each note
        for note in notes:
            vote = note.vote_set.filter(user=user)
            if not vote:
                if randint(0, 4):
                    value = 1
                else:
                    value = -1
                # create vote
                vote = note.vote_set.create(user=user, value=value)
                # add rep
                add_rep(request, v=vote)
        # vote reading
        vote = reading.vote_set.filter(user=user)
        if not vote:
            if randint(0, 4):
                value = 1
            else:
                value = -1
            # create vote
            vote = reading.vote_set.create(user=user, value=value)
            # add rep
            add_rep(request, v=vote)

def first_ten_users():
    """Return the first ten users."""
    return User.objects.all().order_by('date_joined')[0:10]

def random_user():
    """Return a random user."""
    users = first_ten_users()
    return users[randint(0, len(users) - 1)]

def select_first_ten_users():
    """Return list of tuples for first ten users."""
    users = sorted(first_ten_users(), key=lambda u: u.first_name)
    return [(u.pk, u.username) for u in users]