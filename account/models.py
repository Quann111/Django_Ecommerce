from django.db import models
from django.contrib.auth.models import User ,Group
import uuid
# from django.contrib.auth.models import AbstractUser, Group

class Groupp(models.Model):
    GROUP = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.GROUP.name    

class Member(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.IntegerField(blank=True, default=0)
    address = models.CharField(max_length=100, blank=True, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.user.username                                                                                                   