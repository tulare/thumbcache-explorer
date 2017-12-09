# -*- encoding: utf-8 -*-

# python 2/3 compatibility
from __future__ import (
    absolute_import, print_function, division,
    unicode_literals
    )

import os
import six
from struct import unpack, calcsize
from itertools import islice
from collections import namedtuple
from io import BytesIO
from PIL import Image

THMBC_PATH = os.environ['LOCALAPPDATA'] + r'\Microsoft\Windows\Explorer' + '\\'

THMBC_DBS = {
    '32x32' : THMBC_PATH + 'thumbcache_32.db',
    '96x96' : THMBC_PATH + 'thumbcache_96.db',
    '256x256' : THMBC_PATH + 'thumbcache_256.db',
    '1024x1024' : THMBC_PATH + 'thumbcache_1024.db'
}

THMBC_DEFAULT = THMBC_DBS['256x256']

headerFormat = '4s4xIIII'
Header = namedtuple('Header',
    [
    'magic',
    'typeCache',
    'firstEntry',
    'lastEntry',
    'entryCount'
    ])

entryFormat = '4sIQIII4xQQ'
Entry = namedtuple('Entry',
    [
    'offset',
    'magic',
    'cacheSize',
    'entryHash',
    'filenameLength',
    'paddingSize',
    'dataSize',
    'dataChecksum',
    'headerChecksum'
    ])

class Thumbcache(object) :
    def __init__(self, filepathname=THMBC_DEFAULT, cached=False) :
        self.filepathname = filepathname
        
        if cached :
            self.buildCache()
        else :
            self.clearCache()

    def __iter__(self) :
        if self.cached :
            return iter(self.cache.values())
        return ThumbcacheIterator(self)

    def header(self) :
        with open(self.filepathname, 'rb') as fh :
            fh.seek(0)
            return Header._make(unpack(headerFormat, fh.read(calcsize(headerFormat))))

    def checkHeader(self) :
        return self.header().magic == b'CMMM'
    
    def clearCache(self) :
        self.cache = dict()
        self.cached = False

    def buildCache(self) :
        self.clearCache()
        self.cache = dict(enumerate(self))
        self.cached = True

    def count(self) :
        if self.cached :
            return len(self.cache)
        return self.header().entryCount

    def entry(self, index=0) :
        return next(islice(self, index, None), None)

    def checkEntry(self, num=0) :
        return self.entry(num).magic == b'CMMM'

    def checkAllEntries(self) :
        return all(entry.magic == b'CMMM' for entry in self)

    def _data(self, entry) :
        if not entry or entry.magic != b'CMMM' :
            return None
        with open(self.filepathname, 'rb') as fh :
            fh.seek(entry.offset + (entry.cacheSize - entry.dataSize))
            return fh.read(entry.dataSize)

    def getData(self, index=0) :
        return self._data(self.entry(index))

    def _image(self, entry) :
        image_bytes = self._data(entry)
        if not image_bytes :
            return None
        try :
            image = Image.open(BytesIO(image_bytes))
        except OSError as e :
            print(e)
            return None
        
        return image
                
    def getImage(self, index=0) :
        return self._image(self.entry(index))

    def extractImages(self, prefixe='thumb', outdir='.', save=True) :
        with open(self.filepathname, 'rb') as fh :
            for indice, entry in filter(lambda t : t[1].dataSize != 0, enumerate(self)) :
                image = self._image(entry)
                if image :
                    pathname = '{}/{}{:05d}.{}'.format(outdir, prefixe, indice, image.format)
                    print(pathname)
                    if save :
                        image.save(pathname, format=image.format)                

class ThumbcacheIterator(six.Iterator) :
    def __init__(self, thumbcache) :
        self.tc = thumbcache
        self.header = self.tc.header()
        self.position = self.header.firstEntry
        self.current = 0
        
    def __iter__(self) :
        return self

    def __next__(self) :
        if self.header.entryCount == 0 :
            raise StopIteration
        if self.current > self.header.entryCount :
            raise StopIteration
        with open(self.tc.filepathname, 'rb') as fh :
            fh.seek(self.position)
            entry_bytes = fh.read(calcsize(entryFormat))
            if len(entry_bytes) < calcsize(entryFormat) :
                raise StopIteration
            fields = [self.position]
            fields.extend(unpack(entryFormat, entry_bytes))
            entry = Entry._make(fields)
            self.position += entry.cacheSize
            self.current += 1
            return entry
