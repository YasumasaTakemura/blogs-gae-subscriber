import cloudstorage
from google.appengine.ext import ndb
from bs4 import BeautifulSoup


class UrlStateModel(ndb.Model):
    path = ndb.StringProperty()
    created_at = ndb.DateTimeProperty(auto_now_add=True)


class UrlState(UrlStateModel):

    @staticmethod
    def gen_key(key):
        return ndb.Key(UrlState, key[::-1])

    @classmethod
    def get_one(cls, p):
        key = cls.gen_key(p)
        return key.get().to_dict()


def read_file_from_gcs(filename):
    with cloudstorage.open(filename) as f:
        # f.seek(-1024, os.SEEK_END)
        data = f.read()
    return data


def create_file(filename='/test_bucket/test_file.txt'):
    """Create a file."""

    # The retry_params specified in the open call will override the default
    # retry params for this particular file handle.
    write_retry_params = cloudstorage.RetryParams(backoff_factor=1.1)
    data = '<html><a href=/Restaurants_test > url </a><a href=/Attraction_test > url </a></html>'
    try:
        with cloudstorage.open(
                filename, 'w', content_type='text/plain', retry_params=write_retry_params) as f:
            f.write(data)
    except Exception as e:
        print e


def parse(data):
    html = BeautifulSoup(data, "html.parser")
    items = html.find_all('a',href=True)

    def extract(item):
        _item = item['href']
        if _item.startswith('/'):
            _item = _item[1:]
        return _item

    return map(lambda item: extract(item), items)
