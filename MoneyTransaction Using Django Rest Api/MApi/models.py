from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set')
    def save(self, *args, **kwargs):
        if not self.pk: 
            self.set_password(self.password)
        super(User, self).save(*args, **kwargs)

class Wallet(models.Model):
    user=models.ForeignKey('User',on_delete=models.CASCADE,null=True,blank=True)
    # phone_number=models.CharField(max_length=15)
    balance=models.FloatField(null=True,blank=True,default=0)

    def __str__(self):
        return f"wallet - {self.user}"


class Transactions(models.Model):
    wallet=models.ForeignKey('Wallet',on_delete=models.CASCADE)
    sender_phone=models.CharField(max_length=14)
    receiver_phone=models.CharField(max_length=14)
    amount=models.CharField(max_length=100)
    date_time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"transactions - {self.wallet}"
    