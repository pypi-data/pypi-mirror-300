#!/usr/bin/env python3
"""
Copyright (c) 2024 Kyler "Félix" Eastridge

This software is provided 'as-is', without any express or implied
warranty. In no event will the authors be held liable for any damages
arising from the use of this software.

Permission is granted to anyone to use this software for any purpose,
including commercial applications, and to alter it and redistribute it
freely, subject to the following restrictions:

1. The origin of this software must not be misrepresented; you must not
   claim that you wrote the original software. If you use this software
   in a product, an acknowledgment in the product documentation would be
   appreciated but is not required.
2. Altered source versions must be plainly marked as such, and must not be
   misrepresented as being the original software.
3. This notice may not be removed or altered from any source distribution.
"""

import struct
import io
from PIL import Image

def unpackFromStream(strct, stream):
    return strct.unpack_from(stream.read(strct.size))

# Icon decoding
def rgb888_to_rgb565(rgb888):
    r, g, b = rgb888
    return ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)

def rgb565_to_rgb888(rgb565):
    r = (rgb565 >> 11) & 0x1F
    g = (rgb565 >> 5) & 0x3F
    b = rgb565 & 0x1F

    r = (r << 3) | (r >> 2)
    g = (g << 2) | (g >> 4)
    b = (b << 3) | (b >> 2)

    return (r, g, b)

def interleave_bits(x, y):
    result = 0
    for i in range(3):  # 8x8 tile, so max of 3 bits for each coordinate
        result |= ((x >> i) & 1) << (2 * i)     # Interleave x bits
        result |= ((y >> i) & 1) << (2 * i + 1) # Interleave y bits
    return result

def decode_tiled_image(buffer):
    tile_width, tile_height = 8, 8
    order = []

    # Generate Morton/Z-order for an 8x8 tile
    for y in range(tile_height):
        for x in range(tile_width):
            order.append(interleave_bits(x, y))

    # Reorder the buffer according to Morton order
    decoded_buffer = [buffer[order[i]] for i in range(len(order))]
    return decoded_buffer

def reverse_morton_order(buffer):
    order = []

    # Generate Morton/Z-order for an 8x8 tile
    for y in range(8):
        for x in range(8):
            order.append(interleave_bits(x, y))

    # Reverse the Morton ordering
    reversed_buffer = [0] * len(buffer)
    for i, pixel in enumerate(buffer):
        reversed_buffer[order[i]] = pixel

    return reversed_buffer

#https://www.3dbrew.org/wiki/SMDH

# Magic, Version, Reserved
sIconHeader = struct.Struct(">4s H 2x")
# ShortName, LongName, Publisher
sApplicationTitle = struct.Struct(">128s 256s 128s")
# CERO, ESRB, Reserved, USK, PEGI GEN, Reserved, PEGI PRT, PEGI PRT, PEGI BBFC, COB, GRB, CGSRR, Reserved...
sApplicationRating = struct.Struct(">16B")
# RegionMask, JoinGameID, JoinGameMask, FlagsMask, EULAVersion, Reserved, ThumbnailFrame, CecId
sApplicationSettings = struct.Struct(">I IQ I 2B 2x f I")

sIconTile = struct.Struct("<64H")

class CTRIcon:
    # Languages
    LANG_JP = 0
    LANG_EN = 1
    LANG_FR = 2
    LANG_GE = 3
    LANG_IT = 4
    LANG_SP = 5
    LANG_CN = 6
    LANG_KR = 7
    LANG_DU = 8
    LANG_PO = 9
    LANG_RU = 10
    LANG_TW = 11
    # LANG_RESERVED = 12
    # LANG_RESERVED = 13
    # LANG_RESERVED = 14
    # LANG_RESERVED = 15
    # LANG_RESERVED = 16
    LANG_MAX = 16
    
    # Ratings
    RATING_CERO       = 0
    RATING_ESRB       = 1
    # RATING_RESERVED = 2
    RATING_USK        = 3
    RATING_PEGIGEN    = 4
    # RATING_RESERVED = 5
    RATING_PEGIPRT    = 6
    RATING_PEGIBBFC   = 7
    RATING_COB        = 8
    RATING_GRB        = 9
    RATING_CGSRR      = 10
    # RATING_RESERVED = 11
    # RATING_RESERVED = 12
    # RATING_RESERVED = 13
    # RATING_RESERVED = 14
    # RATING_RESERVED = 15
    RATING_MAX = 16
    
    RATING_NONE = 0x20
    RATING_PENDING = 0x40
    RATING_SET = 0x80
    
    # Regions
    REGION_JP = 0x01
    REGION_NA = 0x02
    REGION_EU = 0x04
    REGION_AU = 0x08
    REGION_CN = 0x10
    REGION_KR = 0x20
    REGION_TW = 0x40
    
    # Flags
    FLAG_ULCD = 0x0004
    FLAG_AGREEEULA = 0x0008
    FLAG_AUTOSAVE = 0x0010
    FLAG_AUTOBOOT = 0x0002
    FLAG_EXBANNER = 0x0020
    FLAG_SAVEDATA = 0x0080
    FLAG_DISABLESAVEDATABACKUP = 0x0400
    FLAG_RATINGREQUIRED = 0x0040
    FLAG_SNAKEONLY = 0x1000
    FLAG_ENABLEMIIVERSEJUMPARGS = 0x0100
    
    MAGIC = b"SMDH"
    
    def __init__(self):
        self.version = 0
        
        self.shortName = [""] * self.LANG_MAX
        self.longName = [""] * self.LANG_MAX
        self.publisher = [""] * self.LANG_MAX
        
        self.ratings = [0] * self.RATING_MAX
        
        self.region = 0
        
        self.joinGameID = 0
        self.joinGameMask = 0
        self.flags = 0
        self.EULAVersion = [0, 0]
        self.thumbnailFrame = 0
        self.cecUniqueID = 0
        
        self.ISBN = ""
        self.HTDJH = ""
        self.XCSZ_L = ""
        self.XCSZ_R = ""
        
        self.littleIcon = Image.new("RGB", (24, 24))
        self.bigIcon = Image.new("RGB", (48, 48))
    
    # Decode
    @classmethod
    def fromBytes(cls, data):
        return cls.fromStream(io.BytesIO(data))
    
    @classmethod
    def fromStream(cls, f):
        self = cls()
        magic, version = unpackFromStream(sIconHeader, f)
        if magic != self.MAGIC:
            raise ValueError("Magic did not match!")
        
        if version != 0:
            raise ValueError("Unknown version")
        
        self.version = 0
        
        for i in range(self.LANG_MAX):
            short, long, publisher = unpackFromStream(sApplicationTitle, f)
            if i == self.LANG_CN:
                #Special case for China region
                self.ISBN = long[218:235].decode("ascii").rstrip("\0")
                self.HTDJH = long[235:247].decode("ascii").rstrip("\0")
                self.XCSZ_L = long[247:251].decode("ascii").rstrip("\0")
                self.XCSZ_R = long[251:255].decode("ascii").rstrip("\0")
                long = long[:216]
            
            self.shortName[i], self.longName[i], self.publisher[i] = [
                x.decode("UTF-16-LE").rstrip("\0")
                for x in [short, long, publisher]
            ]
        
        ratings = unpackFromStream(sApplicationRating, f)
        
        for i in range(self.RATING_MAX):
            self.ratings[i] = ratings[i]
        
        self.region, self.joinGameID, self.joinGameMask, \
            self.flags, EULAVersionA, EULAVersionB, self.thumbnailFrame, \
            self.cecUniqueID = unpackFromStream(sApplicationSettings, f)
        
        self.EULAVersion = [EULAVersionA, EULAVersionB]
        
        f.read(0x8) # Reserved
        
        tileBuffer = Image.new("RGB", (8,8))
        tileOffset = 0
        for i in range(0, self.littleIcon.size[0] * self.littleIcon.size[1], 8 * 8):
            tile_data_rgb565 = unpackFromStream(sIconTile, f)
            buffer = [rgb565_to_rgb888(pixel) for pixel in tile_data_rgb565]
            decoded_buffer = decode_tiled_image(buffer)
            tileBuffer.putdata(decoded_buffer)
            self.littleIcon.paste(tileBuffer, ((tileOffset % 3) * 8, (tileOffset // 3) * 8))
            tileOffset += 1
        
        tileOffset = 0
        for i in range(0, self.bigIcon.size[0] * self.bigIcon.size[1], 8 * 8):
            tile_data_rgb565 = unpackFromStream(sIconTile, f)
            buffer = [rgb565_to_rgb888(pixel) for pixel in tile_data_rgb565]
            decoded_buffer = decode_tiled_image(buffer)
            tileBuffer.putdata(decoded_buffer)
            self.bigIcon.paste(tileBuffer, ((tileOffset % 6) * 8, (tileOffset // 6) * 8))
            tileOffset += 1
        
        return self
    
    # Encode
    def __bytes__(self):
        return self.toBytes()
    
    def toBytes(self):
        f = io.BytesIO()
        self.toStream(f)
        return f.getvalue()
    
    def toStream(self, f):
        f.write(sIconHeader.pack(self.MAGIC, self.version))
        
        for i in range(self.LANG_MAX):
            short = self.shortName[i].encode("UTF-16-LE").ljust(128, b"\0")[:128]
            
            if i == self.LANG_CN:
                long = self.longName[i].encode("UTF-16-LE").ljust(218, b"\0")[:218] \
                     + self.HTDJH.encode("ascii").rjust(17, b"\0")[:17] \
                     + self.XCSZ_L.encode("ascii").rjust(12, b"\0")[:12] \
                     + self.XCSZ_L.encode("ascii").rjust(4, b"\0")[:4] \
                     + self.XCSZ_R.encode("ascii").rjust(4, b"\0")[:4]
                
            else:
                long = self.longName[i].encode("UTF-16-LE").ljust(256, b"\0")[:256]
            
            publisher = self.publisher[i].encode("UTF-16-LE").ljust(128, b"\0")[:128]
            
            f.write(sApplicationTitle.pack(short, long, publisher))
        
        f.write(sApplicationRating.pack(*self.ratings))
        
        f.write(sApplicationSettings.pack(
            self.region, self.joinGameID, self.joinGameMask,
            self.flags, self.EULAVersion[0], self.EULAVersion[1], self.thumbnailFrame,
            self.cecUniqueID
        ))
        
        f.write(b"\0" * 8) # Reserved
        
        if self.littleIcon.size != (24, 24) or self.littleIcon.mode != "RGB":
            raise ValueError("LittleIcon must be RGB 24x24")
        
        tileOffset = 0
        for tile_y in range(0, 24, 8):
            for tile_x in range(0, 24, 8):
                tile = self.littleIcon.crop((tile_x, tile_y, tile_x + 8, tile_y + 8))
                tile_data_rgb888 = list(tile.getdata())
                
                for pixel in reverse_morton_order(tile_data_rgb888):
                    rgb565 = rgb888_to_rgb565(pixel)
                    f.write(rgb565.to_bytes(2, byteorder="little"))
                
                tileOffset += 1
        
        if self.bigIcon.size != (48, 48) or self.bigIcon.mode != "RGB":
            raise ValueError("BigIcon must be RGB 48x48")
        
        tileOffset = 0
        for tile_y in range(0, 48, 8):
            for tile_x in range(0, 48, 8):
                tile = self.bigIcon.crop((tile_x, tile_y, tile_x + 8, tile_y + 8))
                tile_data_rgb888 = list(tile.getdata())
                
                for pixel in reverse_morton_order(tile_data_rgb888):
                    rgb565 = rgb888_to_rgb565(pixel)
                    f.write(rgb565.to_bytes(2, byteorder="little"))
                
                tileOffset += 1
    
    # Dicting
    @classmethod
    def fromDict(cls, d):
        self = cls()
        
        if d.get("BigIcon", None):
            if d["BigIcon"].startswith("0x"):
                Image.frombytes("RGB", (48, 48), bytes.fromhex(d["BigIcon"][2:]))
            else:
                self.bigIcon = Image.open(d["BigIcon"])
        
        if d.get("LittleIcon", None):
            if d["LittleIcon"].startswith("0x"):
                Image.frombytes("RGB", (24, 24), bytes.fromhex(d["LittleIcon"][2:]))
            else:
                self.littleIcon = Image.open(d["LittleIcon"])
        
        self.joinGameID = d.get("JoinGameID", 0)
        self.joinGameMask = d.get("JoinGameMask", 0)
        self.cecUniqueID = d.get("CecUniqueID", 0)
        
        self.region = d.get("Region", 0)
        
        if d.get("Ulcd", False):
            self.flags |= self.FLAG_ULCD
        
        if d.get("AgreeEula", False):
            self.flags |= self.FLAG_AGREEEULA
        
        if d.get("AutoSave", False):
            self.flags |= self.FLAG_AUTOSAVE
        
        if d.get("AutoBoot", False):
            self.flags |= self.FLAG_AUTOBOOT
        
        if d.get("ExBanner", False):
            self.flags |= self.FLAG_EXBANNER
        
        if d.get("SaveData", False):
            self.flags |= self.FLAG_SAVEDATA
        
        
        if d.get("DisableSaveDataBackup", False):
            self.flags |= self.FLAG_DISABLESAVEDATABACKUP
        
        if d.get("SNAKEOnly", False):
            self.flags |= self.FLAG_SNAKEONLY
        
        if d.get("EnableMiiverseJumpArgs", False):
            self.flags |= self.FLAG_ENABLEMIIVERSEJUMPARGS
        
        self.longName[self.LANG_JP] = d.get("JPLongName", "")
        self.longName[self.LANG_EN] = d.get("ENLongName", "")
        self.longName[self.LANG_FR] = d.get("FRLongName", "")
        self.longName[self.LANG_GE] = d.get("GELongName", "")
        self.longName[self.LANG_IT] = d.get("ITLongName", "")
        self.longName[self.LANG_SP] = d.get("SPLongName", "")
        self.longName[self.LANG_DU] = d.get("DULongName", "")
        self.longName[self.LANG_PO] = d.get("POLongName", "")
        self.longName[self.LANG_RU] = d.get("RULongName", "")
        self.longName[self.LANG_CN] = d.get("CNLongName", "")
        self.longName[self.LANG_KR] = d.get("KRLongName", "")
        self.longName[self.LANG_TW] = d.get("TWLongName", "")
        
        self.shortName[self.LANG_JP] = d.get("JPShortName", "")
        self.shortName[self.LANG_EN] = d.get("ENShortName", "")
        self.shortName[self.LANG_FR] = d.get("FRShortName", "")
        self.shortName[self.LANG_GE] = d.get("GEShortName", "")
        self.shortName[self.LANG_IT] = d.get("ITShortName", "")
        self.shortName[self.LANG_SP] = d.get("SPShortName", "")
        self.shortName[self.LANG_DU] = d.get("DUShortName", "")
        self.shortName[self.LANG_PO] = d.get("POShortName", "")
        self.shortName[self.LANG_RU] = d.get("RUShortName", "")
        self.shortName[self.LANG_CN] = d.get("CNShortName", "")
        self.shortName[self.LANG_KR] = d.get("KRShortName", "")
        self.shortName[self.LANG_TW] = d.get("TWShortName", "")
        
        self.publisher[self.LANG_JP] = d.get("JPPublisher", "")
        self.publisher[self.LANG_EN] = d.get("ENPublisher", "")
        self.publisher[self.LANG_FR] = d.get("FRPublisher", "")
        self.publisher[self.LANG_GE] = d.get("GEPublisher", "")
        self.publisher[self.LANG_IT] = d.get("ITPublisher", "")
        self.publisher[self.LANG_SP] = d.get("SPPublisher", "")
        self.publisher[self.LANG_DU] = d.get("DUPublisher", "")
        self.publisher[self.LANG_PO] = d.get("POPublisher", "")
        self.publisher[self.LANG_RU] = d.get("RUPublisher", "")
        self.publisher[self.LANG_CN] = d.get("CNPublisher", "")
        self.publisher[self.LANG_KR] = d.get("KRPublisher", "")
        self.publisher[self.LANG_TW] = d.get("TWPublisher", "")
        
        if d.get("RatingRequired", False):
            self.flags |= self.FLAG_RATINGREQUIRED
        
        self.ratings[self.RATING_CERO] = d.get("CERO", "")
        self.ratings[self.RATING_ESRB] = d.get("ESRB", "")
        self.ratings[self.RATING_USK] = d.get("USK", "")
        self.ratings[self.RATING_PEGIGEN] = d.get("PEGI_GEN", "")
        self.ratings[self.RATING_PEGIPRT] = d.get("PEGI_PRT", "")
        self.ratings[self.RATING_PEGIBBFC] = d.get("PEGI_BBFC", "")
        self.ratings[self.RATING_COB] = d.get("COB", "")
        self.ratings[self.RATING_GRB] = d.get("GRB", "")
        self.ratings[self.RATING_CGSRR] = d.get("CGSRR", "")
        
        self.ISBN = d.get("ISBN", "")
        self.HTDJH = d.get("HTDJH", "")
        self.XCSZ_L = d.get("XCSZ_L", "")
        self.XCSZ_R = d.get("XCSZ_R", "")
        
        return self
    
    def toDict(self, bigIcon = None, littleIcon = None):
        if bigIcon == None:
            if self.bigIcon.mode == "RGB" and self.bigIcon.size == (48, 48):
                pixel_data = list(self.bigIcon.getdata())
                if not all(pixel == (0, 0, 0) for pixel in pixel_data):
                    bigIcon = "0x" + self.bigIcon.tobytes().hex().upper()
        
        if littleIcon == None:
            if self.littleIcon.mode == "RGB" and self.littleIcon.size == (24, 24):
                pixel_data = list(self.littleIcon.getdata())
                if not all(pixel == (0, 0, 0) for pixel in pixel_data):
                    littleIcon = "0x" + self.littleIcon.tobytes().hex().upper()
        
        return {
            **({"BigIcon": bigIcon} if bigIcon else {}),
            **({"LittleIcon": littleIcon} if littleIcon else {}),
            
            "JoinGameID": self.joinGameID,
            "JoinGameMask": self.joinGameMask,
            "CecUniqueID": self.cecUniqueID,
            
            "Region": self.region,
            
            "Ulcd": self.flags & self.FLAG_ULCD == self.FLAG_ULCD,
            "AgreeEula": self.flags & self.FLAG_AGREEEULA == self.FLAG_AGREEEULA,
            "AutoSave": self.flags & self.FLAG_AUTOSAVE == self.FLAG_AUTOSAVE,
            "AutoBoot": self.flags & self.FLAG_AUTOBOOT == self.FLAG_AUTOBOOT,
            "ExBanner": self.flags & self.FLAG_EXBANNER == self.FLAG_EXBANNER,
            "SaveData": self.flags & self.FLAG_SAVEDATA == self.FLAG_SAVEDATA,
            
            "DisableSaveDataBackup": self.flags & self.FLAG_DISABLESAVEDATABACKUP == self.FLAG_DISABLESAVEDATABACKUP,
            "SNAKEOnly": self.flags & self.FLAG_SNAKEONLY == self.FLAG_SNAKEONLY,
            "EnableMiiverseJumpArgs": self.flags & self.FLAG_ENABLEMIIVERSEJUMPARGS == self.FLAG_ENABLEMIIVERSEJUMPARGS,
            
            "JPLongName": self.longName[self.LANG_JP],
            "ENLongName": self.longName[self.LANG_EN],
            "FRLongName": self.longName[self.LANG_FR],
            "GELongName": self.longName[self.LANG_GE],
            "ITLongName": self.longName[self.LANG_IT],
            "SPLongName": self.longName[self.LANG_SP],
            "DULongName": self.longName[self.LANG_DU],
            "POLongName": self.longName[self.LANG_PO],
            "RULongName": self.longName[self.LANG_RU],
            "CNLongName": self.longName[self.LANG_CN],
            "KRLongName": self.longName[self.LANG_KR],
            "TWLongName": self.longName[self.LANG_TW],
            
            "JPShortName": self.shortName[self.LANG_JP],
            "ENShortName": self.shortName[self.LANG_EN],
            "FRShortName": self.shortName[self.LANG_FR],
            "GEShortName": self.shortName[self.LANG_GE],
            "ITShortName": self.shortName[self.LANG_IT],
            "SPShortName": self.shortName[self.LANG_SP],
            "DUShortName": self.shortName[self.LANG_DU],
            "POShortName": self.shortName[self.LANG_PO],
            "RUShortName": self.shortName[self.LANG_RU],
            "CNShortName": self.shortName[self.LANG_CN],
            "KRShortName": self.shortName[self.LANG_KR],
            "TWShortName": self.shortName[self.LANG_TW],
            
            "JPPublisher": self.publisher[self.LANG_JP],
            "ENPublisher": self.publisher[self.LANG_EN],
            "FRPublisher": self.publisher[self.LANG_FR],
            "GEPublisher": self.publisher[self.LANG_GE],
            "ITPublisher": self.publisher[self.LANG_IT],
            "SPPublisher": self.publisher[self.LANG_SP],
            "DUPublisher": self.publisher[self.LANG_DU],
            "POPublisher": self.publisher[self.LANG_PO],
            "RUPublisher": self.publisher[self.LANG_RU],
            "CNPublisher": self.publisher[self.LANG_CN],
            "KRPublisher": self.publisher[self.LANG_KR],
            "TWPublisher": self.publisher[self.LANG_TW],
            
            "RatingRequired": self.flags & self.FLAG_RATINGREQUIRED == self.FLAG_RATINGREQUIRED,
            
            "CERO": self.ratings[self.RATING_CERO],
            "ESRB": self.ratings[self.RATING_ESRB],
            "USK": self.ratings[self.RATING_USK],
            "PEGI_GEN": self.ratings[self.RATING_PEGIGEN],
            "PEGI_PRT": self.ratings[self.RATING_PEGIPRT],
            "PEGI_BBFC": self.ratings[self.RATING_PEGIBBFC],
            "COB": self.ratings[self.RATING_COB],
            "GRB": self.ratings[self.RATING_GRB],
            "CGSRR": self.ratings[self.RATING_CGSRR],
            
            "ISBN": self.ISBN,
            "HTDJH": self.HTDJH,
            "XCSZ_L": self.XCSZ_L,
            "XCSZ_R": self.XCSZ_R,
        }
