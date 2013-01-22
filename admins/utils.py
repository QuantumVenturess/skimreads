from django.contrib.auth.models import User
from random import randint

def first_ten_users():
    """Return the first ten users."""
    return User.objects.all().order_by('date_joined')[0:10]


def random_user():
    """Return a random user."""
    return first_ten_users()[randint(0, 9)]