from django.contrib.auth.models import User
import logging
from django.http import HttpRequest

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class EmailAuthBackend:
    def authenticate(self, request: HttpRequest, username: str = None, password: str = None) -> User | None:
        try:
            user = User.objects.get(email=username)
            return user if user.check_password(password) else None
        except (User.MultipleObjectsReturned, User.DoesNotExist) as e:
            logging.warning("El usuario no pudo ser authenticado.")
            logging.info(type(user))
            return None
        
    def get_user(self, user_id: int) -> User | None:
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist as e:
            logging.warning(f"El usuario no existe: {e}")
            return None