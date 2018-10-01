from UserDict import DictMixin
import leveldb
import json


class LevelDict(object, DictMixin):
    """Dict Wrapper around the Google LevelDB Database"""
    def __init__(self, path):
        """Constructor for LevelDict"""
        self.path = path
        self.db = leveldb.LevelDB(self.path)

    def __getitem__(self, key):
        return self.db.Get(key)

    def __setitem__(self, key, value):
        self.db.Put(key, value)

    def __delitem__(self, key):
        self.db.Delete(key)

    def __iter__(self):
        for k in self.db.RangeIter(include_value=False):
            yield k 

    def keys(self):
        return [k for k, v in self.db.RangeIter()]

    def iteritems(self):
        return self.db.RangeIter()

    def rangescan(self, start=None, end=None):
        if start is None and end is None:
            return self.db.RangeIter()
        elif end is None:
            return self.db.RangeIter(start)
        else:
            return self.db.RangeIter(start, end)

class LevelJsonDict(LevelDict):
    """Dict Wrapper around the Google LevelDB Database with JSON serialization"""
    def __getitem__(self, key):
        return json.loads(LevelDict.__getitem__(self, key))

    def __setitem__(self, key, value):
        LevelDict.__setitem__(self, key, json.dumps(value))

    def iteritems(self):
        for k, v in LevelDict.iteritems(self):
            yield k, json.loads(v)

    def rangescan(self, start=None, end=None):
        for k, v in LevelDict.rangescan(self, start, end):
            yield k, json.loads(v)

class LevelPickleDict(LevelDict):
    """Dict Wrapper around the Google LevelDB Database with Pickle serialization"""
    def __getitem__(self, key):
        return pickle.loads(LevelDict.__getitem__(self, key))

    def __setitem__(self, key, value):
        LevelDict.__setitem__(self, key, pickle.dumps(value,protocol=2))

    def iteritems(self):
        for k, v in LevelDict.iteritems(self):
            yield k, pickle.loads(v)

    def rangescan(self, start=None, end=None):
        for k, v in LevelDict.rangescan(self, start, end):
            yield k, pickle.loads(v)
