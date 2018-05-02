from django.conf import settings

from Crypto import Random
import base64

from acclist.lib.crypto.acccrypto import AESCipher, SHA256Hash

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
        seed_string = username + ":" + self.realm + ":" + password
        self.pre_key = SHA256Hash(seed_string).get_bytes()
        aes = AESCipher(self.pre_key, self.key_length, self.mb_encoding)
        self.cipherkey_seed = aes.ecb_decrypt(
            self.true_key, False, False, True)

    def get_bytes(self):
        return self.true_key

    def get_base64_str(self):
        return base64.b64encode(self.true_key).decode("ascii")

    def get_seed_base64_str(self):
        return base64.b64encode(self.cipherkey_seed).decode("ascii")

    def _create_key(self, username, password):
        seed_string = username + ":" + self.realm + ":" + password
        self.pre_key = SHA256Hash(seed_string).get_bytes()
        aes = AESCipher(self.pre_key, self.key_length, self.mb_encoding)
        self.true_key = aes.ecb_encrypt(self.cipherkey_seed, False, True)

class AESEncryptor(object):
    def __init__(self, cipherkey_obj):
        self.aes = AESCipher(
            cipherkey_obj.get_bytes(),
            cipherkey_obj.key_length,
            cipherkey_obj.mb_encoding)

    def enctypt(self, data):
        return self.aes.cbc_encrypt(data, True)

    def decrypt(self, data):
        return self.aes.cbc_decrypt(data, True)

