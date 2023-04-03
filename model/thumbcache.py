# -*- encoding: utf-8 -*-

# python 2/3 compatibility
from __future__ import (
    absolute_import, print_function, division,
    unicode_literals
    )

__all__ = [ 'Thumbcache' ]

import os
import six
from struct import unpack, calcsize
from itertools import islice
from io import BytesIO
from PIL import Image
from model import const as TC

class Thumbcache(object) :
    def __init__(self, filepathname=TC.TC_DBS_DEFAULT, cached=False) :
        self.filepathname = filepathname
        
        if cached :
            self.buildCache()
        else :
            self.clearCache()

    def __iter__(self) :
        if self.cached :
            return iter(self.cache.values())
        return ThumbcacheIterator(self)

    def headerCommon(self) :
        with open(self.filepathname, 'rb') as fh :
            fh.seek(0)
            return TC.HDR_COMMON._make(
                unpack(TC.HDR_COMMON_FMT, fh.read(calcsize(TC.HDR_COMMON_FMT)))
            )

    def header(self) :
        hc = self.headerCommon()

        with open(self.filepathname, 'rb') as fh :
            fh.seek(0)

            if hc.version in (TC.VISTA, TC.W7, TC.W8) :
                return TC.HDR_VISTA78._make(
                    unpack(TC.HDR_VISTA78_FMT, fh.read(calcsize(TC.HDR_VISTA78_FMT)))
                )

            if hc.version in (TC.W8v2,) :
                return TC.HDR_W8V2._make(
                    unpack(TC.HDR_W8V2_FMT, fh.read(calcsize(TC.HDR_W8V2_FMT)))
                )

            if hc.version in (TC.W8v3, TC.W8_1, TC.W10) :
                return TC.HDR_W8V3W10._make(
                    unpack(TC.HDR_W8V3W10_FMT, fh.read(calcsize(TC.HDR_W8V3W10_FMT)))
                )

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
            dataStart = entry.offset + entry.headerSize + entry.filenameLength + entry.paddingSize
            fh.seek(dataStart)
            data = fh.read(entry.dataSize)
            return data

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

        if self.header.version in (TC.VISTA,) :
            self.entry_fmt = TC.ENTRY_VISTA_FMT
            self.entry_cls = TC.ENTRY_VISAT

        if self.header.version in (TC.W7,) :
            self.entry_fmt = TC.ENTRY_W7_FMT
            self.entry_cls = TC.ENTRY_W7

        if self.header.version in (TC.W8v3, TC.W8_1, TC.W10) :
            self.entry_fmt = TC.ENTRY_W8_FMT
            self.entry_cls = TC.ENTRY_W8
        
        self.position = self.header.firstEntry
        self.current = 0
        
    def __iter__(self) :
        return self

    def __next__(self) :
        if self.position == self.header.lastEntry :
            raise StopIteration
        with open(self.tc.filepathname, 'rb') as fh :
            fh.seek(self.position)
            entry_hdr_size = calcsize(self.entry_fmt)
            entry_bytes = fh.read(entry_hdr_size)
            if len(entry_bytes) < entry_hdr_size :
                raise StopIteration
            fields = [self.position, entry_hdr_size]
            fields.extend(unpack(self.entry_fmt, entry_bytes))
            entry = self.entry_cls._make(fields)
            self.position += entry.cacheSize
            self.current += 1
            return entry
