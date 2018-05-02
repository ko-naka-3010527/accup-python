# -*- coding: utf-8 -*-

import base64
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

class AccCrypto(object):
    def _pad(self, s, size):
        l = len(s)
        pad_bytes = (size - l % size) * chr(size - l % size)
        return s + pad_bytes.encode("ascii")

    def _unpad(self, s):
        return s[:-ord(s[len(s)-1:])]

    def _to_bytes(self, s, val_name):
        if type(s) is str:
            return s.encode(self.encode)
        elif type(s) is bytes:
            return s
        else:
            raise TypeError("expected str or bytes as \"" + val_name + "\", " + str(type(s)) + " was given.")

    def _to_str(self, s, val_name):
        if type(s) is str:
            return s
        elif type(s) is bytes:
            return s.decode(self.encode)
        else:
            raise TypeError("expected str or bytes as \"" + val_name + "\", " + str(type(s)) + " was given.")

class AESCipher(AccCrypto):
    def __init__(self, key, key_length_bit=128, encode="utf-8"):
        # initialize
        self.kl_byte = int(key_length_bit / 8)
        self.bs = AES.block_size
        self.encode = encode
        # type check
        key_bytes = self._to_bytes(key, "key")
        # key initialize
        if len(key_bytes) >= self.kl_byte:
            self.key = key_bytes[:self.kl_byte]
        else:
            self.key = self._pad(key_bytes, self.kl_byte)

    def cbc_encrypt(self, pt, base64encode=True):
        pt_bytes = self._to_bytes(pt, "pt")
        pt_raw = self._pad(pt_bytes, self.bs)
        iv = Random.new().read(self.bs)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        cyp_raw = iv + cipher.encrypt(pt_raw)
        if base64encode:
            return base64.b64encode(cyp_raw).decode("ascii")
        else:
            return cyp_raw

    def cbc_decrypt(self, ct, base64encode=True):
        if base64encode:
            ct_raw = base64.b64decode(ct.encode("ascii"))
        else:
            ct_raw = ct
        iv = ct_raw[:self.bs]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        pt_raw = cipher.decrypt(ct_raw[self.bs:])
        pt_str = self._to_str(pt_raw, "pt_raw")
        return self._unpad(pt_str)

    def ecb_encrypt(self, pt, base64encode=True, nopad=False):
        pt_bytes = self._to_bytes(pt, "pt")
        if nopad:
            pt_raw = pt_bytes
        else:
            pt_raw = self._pad(pt_bytes, self.bs)
        cipher = AES.new(self.key, AES.MODE_ECB)
        cyp_raw = cipher.encrypt(pt_raw)
        if base64encode:
            return base64.b64encode(cyp_raw).decode("ascii")
        else:
            return cyp_raw

    def ecb_decrypt(self, ct, base64encode=True, to_str=True, nopad=False):
        if base64encode:
            ct_raw = base64.b64decode(ct.encode("ascii"))
        else:
            ct_raw = ct
        cipher = AES.new(self.key, AES.MODE_ECB)
        if nopad:
            pt_raw = cipher.decrypt(ct_raw)
        else:
            pt_raw = self._unpad(cipher.decrypt(ct_raw))
        if to_str:
            return self._to_str(pt_raw, "pt_raw")
        else:
            return pt_raw

class SHA256Hash(AccCrypto):
    def __init__(self, data, encode="utf-8"):
        self.encode = encode
        data_bytes = self._to_bytes(data, "data")
        self.hashed = SHA256.SHA256Hash(data_bytes)

    def get_bytes(self):
        return self.hashed.digest()

    def get_hexstr(self):
        return self.hashed.hexdigest()

