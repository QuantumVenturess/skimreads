def follow_user(request, user):
    """If current user is logged in and not following user, follow user."""
    # If current user is logged in
    if not request.user.is_anonymous():
        # If current user is not the same as the user
        if request.user.pk is not user.pk:
                # If current user is not already following user
                if not request.user.profile.is_following(user):
                    request.user.follower_set.create(followed=user)

def followed_ids(request):
    """Return id list of users being followed by current user."""
    return [follow.followed.pk for follow in request.user.follower_set.all()]