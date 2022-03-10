from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, BaseUserManager, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from django.db.models import F
from django.db import transaction
from model_utils import Choices

# This class is for overriding default users manager of django user model
class MyAccountManager(BaseUserManager):

    def create_user(self, phone_number, first_name, last_name, country_code, gender, birth_date, avatar, password=None, is_superuser=False, is_staff=False):
        if not phone_number:
            raise ValueError('User must have a phone number')

        user = self.model(
                        phone_number=phone_number,
                        first_name=first_name,
                        last_name=last_name,
                        country_code=country_code,
                        gender=gender,
                        birth_date=birth_date,
                        avatar=avatar,
                        is_staff=is_staff,
                        is_superuser=is_superuser,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    @transaction.atomic
    def create_superuser(self, phone_number, first_name, last_name, country_code, gender, birth_date, avatar, password):
        user = self.create_user(
            phone_number=phone_number,
            password=password,
            first_name=first_name,
            last_name=last_name,
            country_code=country_code,
            gender=gender,
            birth_date=birth_date,
            avatar=avatar,
            is_staff = True,
            is_superuser = True,
        )
        user.save(using = self._db)
        return user

# User Model
class User(AbstractBaseUser, PermissionsMixin):

    GENDER_CHOICES = Choices(
            ('male', 'Male'),
            ('female', 'Female'),
        )

    email = models.EmailField(verbose_name='email', max_length=60, blank=True, null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    country_code = models.CharField(max_length=10)
    phone_number = PhoneNumberField(unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    birth_date = models.DateField()
    avatar = models.ImageField(upload_to="users_images")
    date_joined = models.DateTimeField(verbose_name="Date Joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="Last Login", auto_now=True)
    is_active = models.BooleanField('Active status', default=True)
    is_staff = models.BooleanField('Staff status', default=False)


    objects = MyAccountManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'country_code', 'gender', 'birth_date', 'avatar']

    @transaction.atomic
    def save(self, created=None, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.phone_number)


class Status(models.Model):

    STATUS_CHOICES = Choices(
            ('status1', 'Status 1'),
            ('status2', 'Status 2'),
        )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # All phone number validations performed by PhoneNumberField lib
    phone_number = PhoneNumberField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=10)

    def __str__(self):
          return f'{self.user.phone_number}-{self.status}'
