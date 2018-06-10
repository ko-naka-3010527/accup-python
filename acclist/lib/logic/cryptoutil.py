from django.conf import settings
from django.core.signing import BadSignature, SignatureExpired

from Crypto import Random
import base64
import binascii
import datetime

from acclist.lib.crypto.acccrypto import AESCipher, SHA256Hash

CRYPTOUTIL_COOKIE_SALT_LENGTH = 16
CRYPTOUTIL_COOLIE_PASS_MIN_LENGTH = 32

class CipherKey(object):
    def __init__(self):
        self.realm = settings.CIPHER_REALM
        self.key_length = settings.CIPHER_KEY_LENGTH
        self.cipherkey_seed = None
        self.pre_key = None
        self.mb_encoding = settings.CIPHER_MB_ENCODING
        self.true_key = None

    def generate(self, username, password):
        self.cipherkey_seed = Random.new().read(int(self.key_length / 8))
        self._create_key(username, password)

    def load(self, accuser, username, password):
        self.cipherkey_seed = base64.b64decode(
            accuser.cipherkey.encode("ascii"))
        self._create_key(username, password)

    def update_seed(self, username, password):
        self.set_pre_key(username, password)
        aes = AESCipher(self.pre_key, self.key_length, self.mb_encoding)
        self.cipherkey_seed = aes.ecb_decrypt(
            self.true_key, False, False, True)

    def get_bytes(self):
        return self.true_key

    def get_base64_str(self):
        return base64.b64encode(self.true_key).decode("ascii")

    def get_seed_base64_str(self):
        return base64.b64encode(self.cipherkey_seed).decode("ascii")

    def set_pre_key(self, username, password):
        seed_string = username + ":" + self.realm + ":" + password
        self.pre_key = SHA256Hash(seed_string).get_bytes()
        return self

    def _create_key(self, username, password):
        self.set_pre_key(username, password)
        aes = AESCipher(self.pre_key, self.key_length, self.mb_encoding)
        self.true_key = aes.ecb_encrypt(self.cipherkey_seed, False, True)

class AESEncryptor(object):
    def __init__(self, cipherkey_obj):
        self.aes = AESCipher(
            cipherkey_obj.get_bytes(),
            cipherkey_obj.key_length,
            cipherkey_obj.mb_encoding)

    def encrypt(self, data):
        return self.aes.cbc_encrypt(data, True)

    def decrypt(self, data):
        return self.aes.cbc_decrypt(data, True)

def encrypt_cookie(c):
    # c : str
    if type(c) is not str:
        raise Exception("cookie must be str, given " + str(type(c)))
    key = binascii.unhexlify(settings.COOKIE_ENC_KEY.encode())
    aes = AESCipher(
        key, settings.CIPHER_KEY_LENGTH, settings.CIPHER_MB_ENCODING)
    salt_seed = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    salt = SHA256Hash(salt_seed).get_hexstr()[0:CRYPTOUTIL_COOKIE_SALT_LENGTH]
    plain_bytes = (salt + c).encode(settings.CIPHER_MB_ENCODING)
    return aes.cbc_encrypt(plain_bytes, True)

def decrypt_cookie(c):
    # c : str
    if type(c) is not str:
        raise Exception("cookie must be str, given " + str(type(c)))
    key = binascii.unhexlify(settings.COOKIE_ENC_KEY.encode())
    aes = AESCipher(
        key, settings.CIPHER_KEY_LENGTH, settings.CIPHER_MB_ENCODING)
    return aes.cbc_decrypt(c, True)[CRYPTOUTIL_COOKIE_SALT_LENGTH:]

def encrypt_pass_cookie(pw):
    # pw : str
    if type(pw) is not str:
        raise Exception("cookie must be str, given " + str(type(c)))
    if len(pw) > 254:
        raise Exception("pw length must be shorter than 255 bytes")
    tail_chr = chr(len(pw))
    if len(pw) < CRYPTOUTIL_COOLIE_PASS_MIN_LENGTH:
        pad = "*" * (len(pw) - CRYPTOUTIL_COOLIE_PASS_MIN_LENGTH)
        pad_pw = pw + pad
    else:
        pad_pw = pw
    c_raw = pad_pw + tail_chr
    return encrypt_cookie(c_raw)

def decrypt_pass_cookie(pw):
    # pw : str
    if type(pw) is not str:
        raise Exception("cookie must be str, given " + str(type(c)))
    c_raw = decrypt_cookie(pw)
    return c_raw[:ord(c_raw[-1:])]

def get_encryptor(request, accuser):
    pw_cookie_raw = request.get_signed_cookie(accuser.accup_user_name,
        salt=settings.COOKIE_SIGNED_SALT,
        max_age=settings.COOKIE_MAXAGE)
    pw = decrypt_pass_cookie(pw_cookie_raw)
    ckey = CipherKey()
    ckey.load(accuser, accuser.accup_user_name, pw)
    return AESEncryptor(ckey)

