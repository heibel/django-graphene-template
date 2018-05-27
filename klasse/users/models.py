import uuid

from django_extensions.db.models import TimeStampedModel

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager


class User(TimeStampedModel, AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    middle_name = models.CharField(_("middle name"), max_length=30, blank=True)
    email = models.EmailField(_("email address"), unique=True)
    is_active = models.BooleanField(_("active"), default=False)

    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __unicode__(self):
        return self.get_full_name()
