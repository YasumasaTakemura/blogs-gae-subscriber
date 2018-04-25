
import hashlib

class Hash(object):
    def __init__(self,key):
        self.key = key

    def get_hash(self):
        return hashlib.sha256(self.key).hexdigest()