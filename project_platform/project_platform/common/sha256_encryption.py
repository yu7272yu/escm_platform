# coding=utf-8
import hashlib


class ShaEncryption(object):
    def __init__(self):
        pass

    def add_sha256(self, password, salt):
        try:
            sha256 = hashlib.sha256()
            sha256.update('{}{}'.format(password, salt).encode('utf-8'))
            res = sha256.hexdigest()
        except Exception as e:
            res = password
            print(e)

        return res


if __name__ == '__main__':
    sha_worker = ShaEncryption()
    res = sha_worker.add_sha256('123456', '1acba')
    print(res)
