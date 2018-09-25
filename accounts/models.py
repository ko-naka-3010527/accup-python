from django.db import models

# user management data
class User(models.Model):
    status = models.SmallIntegerField(default=1)
    accup_user_name = models.CharField(max_length=40, unique=True)
    cipherkey = models.CharField(max_length=100)
    createdate = models.DateTimeField(auto_now_add=True)
    modifieddate = models.DateTimeField(auto_now=True)
    deletedate = models.DateTimeField(blank=True, null=True)

# login history
class Userlogin(models.Model):
    accup_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    login_date = models.DateTimeField(auto_now_add=True)
    login_ip = models.GenericIPAddressField()
