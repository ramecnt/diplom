from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.db.models import TextChoices

from .managers import UserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _

NULLABLE = {"blank": True, "null": True}


class UserRoles(TextChoices):
    ADMIN = "admin", _("admin")
    USER = "user", _("user")


class User(AbstractBaseUser):
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_("first name"), max_length=30)
    last_name = models.CharField(_("last name"), max_length=30)
    phone = PhoneNumberField(_("phone number"))
    role = models.CharField(choices=UserRoles.choices, default=UserRoles.USER, max_length=5, verbose_name=_('role'))
    image = models.ImageField(_('avatar'), upload_to='avatars/', **NULLABLE)
    is_active = models.BooleanField(_("is active"), default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', "role"]

    objects = UserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.email

    @property
    def is_admin(self):
        return self.role == UserRoles.ADMIN

    @property
    def is_user(self):
        return self.role == UserRoles.USER

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin
