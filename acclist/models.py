from django.db import models
from django.conf import settings

from accounts.models import User

class Service(models.Model):
    accup_user_id = models.ForeignKey(User,
        on_delete=models.CASCADE)
    service_name = models.CharField(max_length=170)
    # plain text length: 100 bytes

    enc = False
    dec = False

    def encrypt(self, encryptor):
        if self.enc:
            return self
        self.enc = True
        self.dec = False
        self.service_name = encryptor.encrypt(self.service_name)
        return self

    def decrypt(self, encryptor):
        if self.dec:
            return self
        self.dec = True
        self.enc = False
        try:
            self.service_name = encryptor.decrypt(self.service_name)
        except Exception as e:
            self.service_name = settings.CIPHER_FAILURE_STR
        return self

class Mailaddr(models.Model):
    accup_user_id = models.ForeignKey(User,
        on_delete=models.CASCADE, related_name='accup_user',)
    mailaddr_text = models.CharField(max_length=380)
    # plain text length: 254 bytes

    enc = False
    dec = False

    def encrypt(self, encryptor):
        if self.enc:
            return self
        self.enc = True
        self.dec = False
        self.mailaddr_text = encryptor.encrypt(self.mailaddr_text)
        return self

    def decrypt(self, encryptor):
        if self.dec:
            return self
        self.dec = True
        self.enc = False
        try:
            self.mailaddr_text = encryptor.decrypt(self.mailaddr_text)
        except Exception as e:
            self.mailaddr_text = settings.CIPHER_FAILURE_STR
        return self

class Address(models.Model):
    accup_user_id = models.ForeignKey(User,
        on_delete=models.CASCADE)
    address_text = models.CharField(max_length=310)
    # plain text length: 200 bytes

    enc = False
    dec = False

    def encrypt(self, encryptor):
        if self.enc:
            return self
        self.enc = True
        self.dec = False
        self.address_text = encryptor.encrypt(self.address_text)
        return self

    def decrypt(self, encryptor):
        if self.dec:
            return self
        self.dec = True
        self.enc = False
        try:
            self.address_text = encryptor.decrypt(self.address_text)
        except Exception as e:
            self.address_text = settings.CIPHER_FAILURE_STR
        return self

class Phonenum(models.Model):
    accup_user_id = models.ForeignKey(User,
        on_delete=models.CASCADE)
    phonenum_text = models.CharField(max_length=70)
    # plain text length: 20 bytes

    enc = False
    dec = False

    def encrypt(self, encryptor):
        if self.enc:
            return self
        self.enc = True
        self.dec = False
        self.phonenum_text = encryptor.encrypt(self.phonenum_text)
        return self

    def decrypt(self, encryptor):
        if self.dec:
            return self
        self.dec = True
        self.enc = False
        try:
            self.phonenum_text = encryptor.decrypt(self.phonenum_text)
        except Exception as e:
            self.phonenum_text = settings.CIPHER_FAILURE_STR
        return self

class Account(models.Model):
    accup_user_id = models.ForeignKey(User,
        on_delete=models.CASCADE)
    status = models.SmallIntegerField(default=1)
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    name = models.CharField(max_length=170)
    # plain text length: 100 bytes
    passwd = models.CharField(max_length=170)
    # plain text length: 100 bytes
    mailaddr1 = models.ForeignKey(Mailaddr, on_delete=models.PROTECT,
        related_name='mail_1', blank=True, null=True)
    mailaddr2 = models.ForeignKey(Mailaddr, on_delete=models.PROTECT,
        related_name='mail_2', blank=True, null=True)
    mailaddr3 = models.ForeignKey(Mailaddr, on_delete=models.PROTECT,
        related_name='mail_3', blank=True, null=True)
    address = models.ForeignKey(Address,
        on_delete=models.PROTECT, blank=True, null=True)
    phonenum = models.ForeignKey(Phonenum,
        on_delete=models.PROTECT, blank=True, null=True)
    link1 = models.ForeignKey('self', on_delete=models.SET_NULL,
        related_name='account_link_1', blank=True, null=True)
    link2 = models.ForeignKey('self', on_delete=models.SET_NULL,
        related_name='account_link_2', blank=True, null=True)
    link3 = models.ForeignKey('self', on_delete=models.SET_NULL,
        related_name='account_link_3', blank=True, null=True)
    multifactorauth_type = models.CharField(
        max_length=170, blank=True, null=True)
    multifactorauth_id = models.CharField(
        max_length=170, blank=True, null=True)
    # plain text length: 100 bytes
    secret_q1 = models.CharField(max_length=310, blank=True, null=True)
    secret_a1 = models.CharField(max_length=310, blank=True, null=True)
    secret_q2 = models.CharField(max_length=310, blank=True, null=True)
    secret_a2 = models.CharField(max_length=310, blank=True, null=True)
    secret_q3 = models.CharField(max_length=310, blank=True, null=True)
    secret_a3 = models.CharField(max_length=310, blank=True, null=True)
    # plain text length: 200 bytes
    account_register_date = models.DateField(blank=True, null=True)
    account_unregister_date = models.DateField(blank=True, null=True)
    memo = models.TextField(blank=True, null=True)
    createdate = models.DateTimeField(auto_now_add=True)
    modifieddate = models.DateTimeField(auto_now=True)
    deletedate = models.DateTimeField(blank=True, null=True)

    enc = False
    dec = False

    def encrypt(self, encryptor):
        if self.enc:
            return self
        self.enc = True
        self.dec = False
        self.service = self.service.encrypt(encryptor)
        self.name = encryptor.encrypt(self.name)
        self.passwd = encryptor.encrypt(self.passwd)
        if self.mailaddr1 is not None:
            self.mailaddr1 = self.mailaddr1.encrypt(encryptor)
        if self.mailaddr2 is not None:
            self.mailaddr2 = self.mailaddr2.encrypt(encryptor)
        if self.mailaddr3 is not None:
            self.mailaddr3 = self.mailaddr3.encrypt(encryptor)
        if self.address is not None:
            self.address = self.address.encrypt(encryptor)
        if self.phonenum is not None:
            self.phonenum = self.phonenum.encrypt(encryptor)
        if self.link1 is not None:
            self.link1 = self.link1.encrypt(encryptor)
        if self.link2 is not None:
            self.link2 = self.link2.encrypt(encryptor)
        if self.link3 is not None:
            self.link3 = self.link3.encrypt(encryptor)
        if self.multifactorauth_type is not None:
            self.multifactorauth_type = encryptor.encrypt(
                self.multifactorauth_type)
        if self.multifactorauth_id is not None:
            self.multifactorauth_id = encryptor.encrypt(
                self.multifactorauth_id)
        if self.secret_q1 is not None:
            self.secret_q1 = encryptor.encrypt(self.secret_q1)
        if self.secret_a1 is not None:
            self.secret_a1 = encryptor.encrypt(self.secret_a1)
        if self.secret_q2 is not None:
            self.secret_q2 = encryptor.encrypt(self.secret_q2)
        if self.secret_a2 is not None:
            self.secret_a2 = encryptor.encrypt(self.secret_a2)
        if self.secret_q3 is not None:
            self.secret_q3 = encryptor.encrypt(self.secret_q3)
        if self.secret_a3 is not None:
            self.secret_a3 = encryptor.encrypt(self.secret_a3)
        if self.memo is not None:
            self.memo = encryptor.encrypt(self.memo)
        return self

    def decrypt(self, encryptor):
        if self.dec:
            return self
        self.dec = True
        self.enc = False
        self.service = self.service.decrypt(encryptor)
        try: 
            self.name = encryptor.decrypt(self.name)
        except Exception as e:
            self.name = settings.CIPHER_FAILURE_STR
        try:
            self.passwd = encryptor.decrypt(self.passwd)
        except Exception as e:
            self.passwd = settings.CIPHER_FAILURE_STR
        if self.mailaddr1 is not None:
            self.mailaddr1 = self.mailaddr1.decrypt(encryptor)
        if self.mailaddr2 is not None:
            self.mailaddr2 = self.mailaddr2.decrypt(encryptor)
        if self.mailaddr3 is not None:
            self.mailaddr3 = self.mailaddr3.decrypt(encryptor)
        if self.address is not None:
            self.address = self.address.decrypt(encryptor)
        if self.phonenum is not None:
            self.phonenum = self.phonenum.decrypt(encryptor)
        if self.link1 is not None:
            self.link1 = self.link1.decrypt(encryptor)
        if self.link2 is not None:
            self.link2 = self.link2.decrypt(encryptor)
        if self.link3 is not None:
            self.link3 = self.link3.decrypt(encryptor)
        if self.multifactorauth_type is not None:
            try:
                self.multifactorauth_type = encryptor.decrypt(
                    self.multifactorauth_type)
            except Exception as e:
                self.multifactorauth_type = settings.CIPHER_FAILURE_STR
        if self.multifactorauth_id is not None:
            try:
                self.multifactorauth_id = encryptor.decrypt(
                    self.multifactorauth_id)
            except Exception as e:
                self.multifactorauth_id = settings.CIPHER_FAILURE_STR
        if self.secret_q1 is not None:
            try:
                self.secret_q1 = encryptor.decrypt(self.secret_q1)
            except Exception as e:
                self.secret_q1 = settings.CIPHER_FAILURE_STR
        if self.secret_a1 is not None:
            try:
                self.secret_a1 = encryptor.decrypt(self.secret_a1)
            except Exception as e:
                self.secret_a1 = settings.CIPHER_FAILURE_STR
        if self.secret_q2 is not None:
            try:
                self.secret_q2 = encryptor.decrypt(self.secret_q2)
            except Exception as e:
                self.secret_q2 = settings.CIPHER_FAILURE_STR
        if self.secret_a2 is not None:
            try:
                self.secret_a2 = encryptor.decrypt(self.secret_a2)
            except Exception as e:
                self.secret_a2 = settings.CIPHER_FAILURE_STR
        if self.secret_q3 is not None:
            try:
                self.secret_q3 = encryptor.decrypt(self.secret_q3)
            except Exception as e:
                self.secret_q3 = settings.CIPHER_FAILURE_STR
        if self.secret_a3 is not None:
            try:
                self.secret_a3 = encryptor.decrypt(self.secret_a3)
            except Exception as e:
                self.secret_a3 = settings.CIPHER_FAILURE_STR
        if self.memo is not None:
            try:
                self.memo = encryptor.decrypt(self.memo)
            except Exception as e:
                self.memo = settings.CIPHER_FAILURE_STR
        return self

