from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class UserManager(BaseUserManager):

    def create_user(self, id_token, access_token=None, password=None,
                    is_active=None, is_staff=False, is_admin=False):
        """
        Creates and saves a User with the given email and password.
        """
        if not id_token:
            raise ValueError('Users must have id_token')

        user = self.model(
            id_token=id_token,
            access_token=access_token,
        )

        user.set_unusable_password()
        user.active = is_active
        user.staff = is_staff
        user.admin = is_admin
        user.save(using=self._db)
        return user

    def create_staffuser(self, id_token, access_token, password=None):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.model(
            id_token=id_token,
            access_token=access_token,
        )
        user.set_unusable_password()
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, id_token, access_token, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.model(
            id_token=id_token,
            access_token=access_token,
        )
        user.set_unusable_password()
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    id_token = models.TextField(
        verbose_name='id token',
        unique=True,
    )
    access_token = models.TextField(null=True)

    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'id_token'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        # The user is identified by their id token
        return self.id_token

    def get_short_name(self):
        # The user is identified by their id token
        return self.id_token

    def __str__(self):              # __unicode__ on Python 2
        return self.id_token

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active
