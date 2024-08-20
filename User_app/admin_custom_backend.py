from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from DjangoProject.crypto import encrypt, decrypt


class LoginBackend(ModelBackend):
    """ Custom authentication backend that allows login using username or email or phone etc."""
    def authenticate(self, request, username, password=None, **kwargs):
        User = get_user_model()
        email = username  # get email from username
        try:
            for user in User.objects.all(): # get all users
                if decrypt(user.email) == email:    # decrypt email
                    return user
        except User.DoesNotExist:
            return None

        ''' check user is not None, user is active, user is superuser(admin) and user is not deleted.'''
        if (user is not None) and (user.is_active) and (user.is_superuser) and not(user.isDeleted):
            if user.check_password(password):   # check password
                return user
        return None



