class AcccryptoDecryptException(Exception):
    def __init__(self, dectype):
        self.message = "decryption failue (" + dectype + ")"

