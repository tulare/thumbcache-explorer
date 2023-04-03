__all__ = [ 'TC_DBS', 'TC_DBS_DEFAULT' ]

import os
from collections import namedtuple

TC_PATH = os.environ['LOCALAPPDATA'] + r'\Microsoft\Windows\Explorer' + '\\'

TC_DBS = {
    'thmb16' : TC_PATH + 'thumbcache_16.db',
    'thmb32' : TC_PATH + 'thumbcache_32.db',
    'thmb48' : TC_PATH + 'thumbcache_48.db',
    'thmb96' : TC_PATH + 'thumbcache_96.db',
    'thmb256' : TC_PATH + 'thumbcache_256.db',
    'thmb768' : TC_PATH + 'thumbcache_768.db',
    'thmb1024' : TC_PATH + 'thumbcache_1024.db',
    'thmb1280' : TC_PATH + 'thumbcache_1280.db',
    'thmb1920' : TC_PATH + 'thumbcache_1920.db',
    'thmb2560' : TC_PATH + 'thumbcache_2560.db',
    'thmb_stream' : TC_PATH + 'thumbcache_custom_stream.db',
    'thmb_exif' : TC_PATH + 'thumbcache_exif.db',
    'thmb_sr' : TC_PATH + 'thumbcache_sr.db',
    'thmb_wide' : TC_PATH + 'thumbcache_wide.db',
    'thmb_widealt' : TC_PATH + 'thumbcache_wide_alternate.db',
    'icon16' : TC_PATH + 'iconcache_16.db',
    'icon32' : TC_PATH + 'iconcache_32.db',
    'icon48' : TC_PATH + 'iconcache_48.db',
    'icon96' : TC_PATH + 'iconcache_96.db',
    'icon256' : TC_PATH + 'iconcache_256.db',
    'icon768' : TC_PATH + 'iconcache_768.db',
    'icon1280' : TC_PATH + 'iconcache_1280.db',
    'icon1920' : TC_PATH + 'iconcache_1920.db',
    'icon2560' : TC_PATH + 'iconcache_2560.db',
    'icon_stream' : TC_PATH + 'iconcache_custom_stream.db',
    'icon_exif' : TC_PATH + 'iconcache_exif.db',
    'icon_sr' : TC_PATH + 'iconcache_sr.db',
    'icon_wide' : TC_PATH + 'iconcache_wide.db',
    'icon_widealt' : TC_PATH + 'iconcache_wide_alternate.db',    
}

TC_DBS = {
    k : v
    for k,v in TC_DBS.items()
    if os.path.isfile(v) and os.stat(v).st_size > 24
}

TC_DBS_DEFAULT = TC_DBS['thmb256']

#

VISTA = 0x14
W7    = 0x15
W8    = 0x1A
W8v2  = 0x1C
W8v3  = 0x1E
W8_1  = 0x1F
W10   = 0x20

#

HDR_COMMON_FMT = '4sII'
HDR_COMMON = namedtuple('HeaderCommon', [
    'magic',
    'version',
    'type'
])

HDR_VISTA78_FMT = '4sIIIII'
HDR_VISTA78 = namedtuple('HeaderVista78', [
    'magic',
    'version',
    'type',
    'firstEntry',
    'lastEntry',
    'entryCount',
])

HDR_W8V2_FMT = '4sIIIIII'
HDR_W8V2 = namedtuple('Header8v2', [
    'magic',
    'version',
    'type',
    'unknown',
    'firstEntry',
    'lastEntry',
    'entryCount',
])

HDR_W8V3W10_FMT = '4sIIIII'
HDR_W8V3W10 = namedtuple('HeaderW8vW310', [
    'magic',
    'version',
    'type',
    'unknown',
    'firstEntry',
    'lastEntry',
])

ENTRY_W7_FMT = '4sIQIIIIQQ'
ENTRY_W7 = namedtuple('EntryW7', [
    'offset',
    'headerSize',
    'magic',
    'cacheSize',
    'entryHash',
    'filenameLength',
    'paddingSize',
    'dataSize',
    'unknown',
    'dataChecksum',
    'headerChecksum'
])

ENTRY_W8_FMT = '4sIQIIIIIIQQ'
ENTRY_W8 = namedtuple('EntryW8', [
    'offset',
    'headerSize',
    'magic',
    'cacheSize',
    'entryHash',
    'filenameLength',
    'paddingSize',
    'dataSize',
    'width',
    'height',
    'unknown',
    'dataChecksum',
    'headerChecksum'
])

ENTRY_VISTA_FMT = '4sIQ4sIIIIQQ'
ENTRY_VISTA = namedtuple('EntryVista', [
    'offset',
    'headerSize',
    'magic',
    'cacheSize',
    'entryHash',
    'extension',
    'filenameLength',
    'paddingSize',
    'dataSize',
    'unknown',
    'dataChecksum',
    'headerChecksum'
])
