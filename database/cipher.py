

class Cipher(object):

    def __init__(self):
        pass

    def encrypt(self, data, key):
        encrypted = aes_encrypt(data, key)
        return encrypted

    def decrypt(self, data, key):
        decrypted = aes_decrypt(data, key)
        return decrypted

    def derive_key(self, master_password):
        pass_hash = sha256(master_password)
        rand_salt = urandom()
        key = argon2(pass_hash, rand_salt)
        return key
