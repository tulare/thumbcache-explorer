# -*- encoding: utf-8 -*-

__all__ = [ 'Model' ]

from helpers.observer import Observable
from model.const import TC_DBS_DEFAULT
from model.thumbcache import Thumbcache

class Model(Observable) :

    def __init__(self) :
        super(Model, self).__init__()
        self.cache = None
        self.entries = []

    def sync(self) :
        self.notify('populate', entries=self.entries)

    def build(self, cachefile=TC_DBS_DEFAULT, empty=False) :
        self.entries = []
        self.cache = Thumbcache(cachefile, cached=True)
        for indice, entry in enumerate(self.cache) :
            # filter empty ?
            if not empty and entry.dataSize == 0 :
                continue
            elem = (indice, entry.offset, '{:016x}'.format(entry.entryHash), entry.dataSize)
            self.entries.append(elem)
        self.sync()

    def getImage(self, index) :
        return self.cache.getImage(index)

