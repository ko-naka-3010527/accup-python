from django.db import models

# user management data
class User(models.Model):
    status = models.SmallIntegerField(default=1)
    accup_user_name = models.CharField(max_length=40)
    mailaddr = models.EmailField(unique=True)
    passwd = models.CharField(max_length=100)
    cipherkey = models.CharField(max_length=100)
    createdate = models.DateTimeField(auto_now_add=True)
    modifieddate = models.DateTimeField(auto_now=True)
    deletedate = models.DateTimeField(blank=True, null=True)

class Token(models.Model):
    accup_user_id = models.OneToOneField(User,
        on_delete=models.CASCADE, unique=True)
    token = models.CharField(max_length=100)
    issued = models.DateTimeField()
    expire = models.DateTimeField()

# account data
class Service(models.Model):
    accup_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    service_name = models.CharField(max_length=100)

class Mailaddr(models.Model):
    accup_user_id = models.ForeignKey(User,
        on_delete=models.CASCADE, related_name='accup_user',)
    mailaddr_text = models.EmailField(unique=True)

class Address(models.Model):
    accup_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    address_text = models.CharField(max_length=200, unique=True)

class Phonenum(models.Model):
    accup_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    phonenum_text = models.CharField(max_length=20, unique=True)

class Account(models.Model):
    accup_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
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
    multifactorauth_type = models.IntegerField(blank=True, null=True)
    multifactorauth_id = models.IntegerField(blank=True, null=True)
    account_register_date = models.DateField(blank=True, null=True)
    account_unregister_date = models.DateField(blank=True, null=True)
    createdate = models.DateTimeField(auto_now_add=True)
    modifieddate = models.DateTimeField(auto_now=True)
    deletedate = models.DateTimeField(blank=True, null=True)
    
