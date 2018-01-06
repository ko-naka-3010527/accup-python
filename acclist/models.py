from django.db import models
from accounts.models import User

# account data
class Service(models.Model):
    accup_user_id = models.ForeignKey(User,
        on_delete=models.CASCADE)
    service_name = models.CharField(max_length=100)

class Mailaddr(models.Model):
    accup_user_id = models.ForeignKey(User,
        on_delete=models.CASCADE, related_name='accup_user',)
    mailaddr_text = models.EmailField()

class Address(models.Model):
    accup_user_id = models.ForeignKey(User,
        on_delete=models.CASCADE)
    address_text = models.CharField(max_length=200)

class Phonenum(models.Model):
    accup_user_id = models.ForeignKey(User,
        on_delete=models.CASCADE)
    phonenum_text = models.CharField(max_length=20)

class Account(models.Model):
    accup_user_id = models.ForeignKey(User,
        on_delete=models.CASCADE)
    status = models.SmallIntegerField(default=1)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    passwd = models.CharField(max_length=100)
    mailaddr1 = models.ForeignKey(Mailaddr, on_delete=models.CASCADE,
        related_name='mail_1', blank=True, null=True)
    mailaddr2 = models.ForeignKey(Mailaddr, on_delete=models.CASCADE,
        related_name='mail_2', blank=True, null=True)
    mailaddr3 = models.ForeignKey(Mailaddr, on_delete=models.CASCADE,
        related_name='mail_3', blank=True, null=True)
    address = models.ForeignKey(Address,
        on_delete=models.CASCADE, blank=True, null=True)
    phonenum = models.ForeignKey(Phonenum,
        on_delete=models.CASCADE, blank=True, null=True)
    link1 = models.ForeignKey('self', on_delete=models.CASCADE,
        related_name='account_link_1', blank=True, null=True)
    link2 = models.ForeignKey('self', on_delete=models.CASCADE,
        related_name='account_link_2', blank=True, null=True)
    link3 = models.ForeignKey('self', on_delete=models.CASCADE,
        related_name='account_link_3', blank=True, null=True)
    multifactorauth_type = models.CharField(
        max_length=100, blank=True, null=True)
    multifactorauth_id = models.CharField(
        max_length=100, blank=True, null=True)
    secret_q1 = models.CharField(max_length=200, blank=True, null=True)
    secret_a1 = models.CharField(max_length=200, blank=True, null=True)
    secret_q2 = models.CharField(max_length=200, blank=True, null=True)
    secret_a2 = models.CharField(max_length=200, blank=True, null=True)
    secret_q3 = models.CharField(max_length=200, blank=True, null=True)
    secret_a3 = models.CharField(max_length=200, blank=True, null=True)
    account_register_date = models.DateField(blank=True, null=True)
    account_unregister_date = models.DateField(blank=True, null=True)
    createdate = models.DateTimeField(auto_now_add=True)
    modifieddate = models.DateTimeField(auto_now=True)
    deletedate = models.DateTimeField(blank=True, null=True)
