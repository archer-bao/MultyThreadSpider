import hashlib


def encrypt_md5(src):
    m2 = hashlib.md5()
    m2.update(bytes(src, encoding="utf8"))
    return m2.hexdigest().upper()
