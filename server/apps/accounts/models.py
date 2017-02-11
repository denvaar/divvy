import uuid

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.contrib.auth.hashers import is_password_usable

from model_utils.managers import InheritanceManagerMixin


class BaseUserManager(InheritanceManagerMixin, BaseUserManager):

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(
            email=email, is_staff=is_staff, is_active=True,
            is_superuser=is_superuser, last_login=now, date_joined=now,
            **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class BaseUser(AbstractBaseUser, PermissionsMixin):

    '''
    An abstract base class implementing a fully featured User model
    with admin-compliant permissions.
    '''
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
    )
    uuid = models.SlugField(default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    is_staff = models.BooleanField(
        default=False,
        help_text='Designates whether the user can log into this admin '
                    'site.')
    is_active = models.BooleanField(
        default=True,
        help_text='Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.') 

    objects = BaseUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def save(self, *args, **kwargs):
        if not is_password_usable(self.password):
            self.set_password(self.password)
        return super(BaseUser, self).save(*args, **kwargs)

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()


class AppUser(BaseUser):
    accounts = models.ManyToManyField('Account', blank=True,
                                      related_name='app_users')
    objects = BaseUserManager()


class Account(models.Model):
    name = models.CharField(max_length=254)
    created = models.DateTimeField(auto_now_add=True) 
    fi = models.CharField(max_length=254) # TODO make secure
    userid = models.CharField(max_length=254)
    userpass = models.CharField(max_length=254)
    acctid = models.CharField(max_length=254)
    balance = models.DecimalField(max_digits=14, decimal_places=2, default=0.0)

    def __str__(self):
        return self.name


