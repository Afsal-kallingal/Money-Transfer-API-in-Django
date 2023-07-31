from django.contrib.auth.backends import BaseBackend
from .models import User

class CustomUserModelBackend(BaseBackend):
    def authenticate(self, request, phone_number=None, password=None):
        try:
            user = User.objects.get(phone_number=phone_number)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None