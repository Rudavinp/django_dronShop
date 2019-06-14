from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, AbstractUser, PermissionsMixin,
                                        BaseUserManager)


class Address(models.Model):
	firs_name = models.CharField(max_length=256, blank=True)
	last_name = models.CharField(max_length=256, blank=True)
	company_name = models.CharField(max_length=256, blank=True)
	street_addres_1 = models.CharField(max_length=256, blank=True)
	street_addres_2 = models.CharField(max_length=256, blank=True)
	city = models.CharField(max_length=256, blank=True)
	city_area = models.CharField(max_length=256, blank=True)
	postal_code = models.CharField(max_length=6, blank=True)
	phonenumber = models.CharField(max_length=9, blank=True)



class UserManager(BaseUserManager):

	def create_user(
			self, email, password=None, is_staff=False, is_active=True,
			**extra_fields):
		email = UserManager.normalize_email(email)

		user = self.model(
			email=email, is_active=is_active, is_staff=is_staff,
			**extra_fields
		)
		if password:
			print(0, password)
			user.set_password(password)
		user.save()
		return user

	def create_superuser(self, email, password=None, **extra_fields):
		return self.create_user(
			email, password, is_staff=True, is_superuser=True, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(unique=True)
	is_staff = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	addresses = models.ManyToManyField(
		Address, blank=True, related_name='user_addresses')

	USERNAME_FIELD = 'email'

	objects = UserManager()


	def get_full_name(self):
		return self.email



# Create your models here.
