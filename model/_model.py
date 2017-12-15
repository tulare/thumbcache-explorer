# -*- encoding: utf-8 -*-

from helpers.observer import Observable
from model.thumbcache import THMBC_DBS, Thumbcache

class Model(Observable) :

    def __init__(self) :
        super(Model, self).__init__()
        self.cache = None
        self.entries = []

    def sync(self) :
        self.notify('populate', entries=self.entries)

    def build(self, cachefile=THMBC_DBS['256x256'], empty=False) :
        self.entries = []
        self.cache = Thumbcache(cachefile, cached=True)
        for indice, entry in enumerate(self.cache) :
            # filter empty ?
            if not empty and entry.dataSize == 0 :
                continue
            elem = (indice, hex(entry.entryHash), entry.dataSize)
            self.entries.append(elem)
        self.sync()

    def getImage(self, index) :
        return self.cache.getImage(index)

