from django.contrib.contenttypes.models import ContentType
from . import models

def create_action(user, verb, target=None):
    action = models.Action(user=user, verb=verb, target=target)
    action.save()