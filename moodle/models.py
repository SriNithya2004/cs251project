from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
ROLES = (
    (1, 'student'),
    (2, 'instructor')
)

class User(AbstractUser):
    role = models.PositiveSmallIntegerField(choices=ROLES)