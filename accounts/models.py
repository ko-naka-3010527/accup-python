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

