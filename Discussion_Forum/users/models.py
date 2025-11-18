from django.db import models
from django.contrib.auth.models import AbstractUser

class USER(AbstractUser):
    # empty by now

    def __str__(self):
        return self.username