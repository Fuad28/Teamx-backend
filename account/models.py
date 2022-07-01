from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser,  BaseUserManager, PermissionsMixin, UserManager



class UserManager(BaseUserManager):
	def create_user(self, email, full_name, password, **other_fields):
		"""Creates and saves a User with the given email, full name, and password."""

		if not email:
			raise ValueError(_('Please enter an email address'))

		email= self.normalize_email(email)
		user= self.model(email=email, full_name=full_name, **other_fields)
		user.set_password(password)
		user.save()
		return user

	
	def create_superuser(self, email, full_name,  password, **other_fields):
		"""Creates and saves a superuser with the given email,full name and password. Also sets is_staff to true"""
		user= self.create_user(email, full_name, password, **other_fields)
		user.is_staff=True
		user.is_active=True
		user.is_superuser=True
		user.save()
		return user
class User(AbstractUser, PermissionsMixin):
	username = None
	email= models.EmailField(unique=True, blank= False)
	full_name= models.CharField(max_length=30, blank=False, null=False)
	slug= models.SlugField(max_length=200)
	is_verified= models.BooleanField(default=False)
	is_blocked= models.BooleanField(default=False)
	is_active= models.BooleanField(default=False)

	USERNAME_FIELD= "email"
	REQUIRED_FIELDS= ["full_name"]
	objects= UserManager()

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		self.slug= slugify(self.full_name)

class Profile(models.Model):
	user= models.OneToOneField(User, on_delete= models.CASCADE)
	image= models.URLField(null=True, blank=True)
	biography= models.TextField(blank=True, null=True)
	language= models.CharField(max_length=30, default= "english")
	date_of_birth= models.DateField(null=True, blank=True)
	country= models.CharField(max_length=30, null= True)
	phone= models.CharField(max_length=11, blank=True, null= True)
	twitter_profile= models.URLField(null=True, blank=True, help_text= "Twitter profile username or link")
	linkedln_profile= models.URLField(null=True, blank=True, help_text= "Linkedln profile username or link")
	website= models.URLField(null=True, blank=True, help_text= "website or another social media profile link")


	def __str__(self):
		return f"{self.user.first_name} {self.user.last_name} profile"


