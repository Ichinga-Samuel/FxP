from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail


U = settings.AUTH_USER_MODEL


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, active=True, admin=False, staff=False):
        if not email: raise ValueError("User must have a valid email address")
        if not password: raise ValueError("Password must be set")
        user_obj = self.model(
            email=self.normalize_email(email),
            is_active=active,
            admin=admin,
            staff=staff
        )
        user_obj.set_password(password)
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, password=None):
        user = self.create_user(email, password, staff=True)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password, staff=True, admin=True)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    joined = models.DateTimeField(auto_now_add=True)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):

        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_superuser(self):
        return self.admin

    @property
    def is_staff(self):
        return self.staff


class Profile(models.Model):
    user = models.OneToOneField(U, on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)
    subscribed = models.BooleanField(default=False)
    username = models.CharField(max_length=255, blank=True)
    firstName = models.CharField(max_length=255, blank=True)
    lastName = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'{self.user.email}'


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
