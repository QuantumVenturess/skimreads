from django.contrib.admin.models import User
from django.contrib.auth.backends import ModelBackend

class EmailAuthBackend(ModelBackend):
    def authenticate(self, email=None, password=None):
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

class FacebookAuthBackend(ModelBackend):
    def authenticate(self, email):
        try:
            user = User.objects.get(email=email)
            return user
        except User.DoesNotExist:
            return None