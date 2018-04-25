import os
import re
import cloudstorage
from google.appengine.ext import ndb
from bs4 import BeautifulSoup


class UrlStateModel(ndb.Model):
    path = ndb.StringProperty()
    created_at = ndb.DateTimeProperty(auto_now_add=True)


class UrlState(UrlStateModel):
    @staticmethod
    def reverse_id(key):
        return key[::-1]


    @classmethod
    def get_one(cls, p):
        key = cls.reverse_id(p)
        return cls.get_by_id(key)


def read_file_from_gcs(filename):
    with cloudstorage.open(filename) as f:
        f.seek(-1024, os.SEEK_END)
        data = f.read()
    return data


def parse(data):
    html = BeautifulSoup(data)
    word = '/Restaurant'
    res = html.find_all(href=re.compile(word))
    return res
