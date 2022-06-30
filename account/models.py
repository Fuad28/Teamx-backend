from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email= models.EmailField(unique=True, blank= False)

    USERNAME_FIELD= "email"
    REQUIRED_FIELDS= ["first_name", "last_name"]

class Profile(models.Model):
    user= models.OneToOneField(User, on_delete= models.CASCADE)
    image= models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} profile"

