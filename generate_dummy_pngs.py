import struct
import zlib
import os

def create_transparent_png(filename, width=512, height=512):
    # A simple 1x1 transparent PNG, scaled or just 1x1 is fine since we just need a valid PNG.
    # Let's write a standard 1x1 transparent PNG
    png_magic = b'\x89PNG\r\n\x1a\n'
    
    # IHDR
    ihdr_data = struct.pack("!IIBBBBB", 1, 1, 8, 6, 0, 0, 0)
    ihdr_crc = zlib.crc32(b'IHDR' + ihdr_data) & 0xffffffff
    ihdr = struct.pack("!I", len(ihdr_data)) + b'IHDR' + ihdr_data + struct.pack("!I", ihdr_crc)
    
    # IDAT
    # 1 pixel, RGBA = 0,0,0,0. Filter byte = 0. So 5 bytes of uncompressed data: \x00\x00\x00\x00\x00
    idat_data = zlib.compress(b'\x00\x00\x00\x00\x00')
    idat_crc = zlib.crc32(b'IDAT' + idat_data) & 0xffffffff
    idat = struct.pack("!I", len(idat_data)) + b'IDAT' + idat_data + struct.pack("!I", idat_crc)
    
    # IEND
    iend_data = b''
    iend_crc = zlib.crc32(b'IEND' + iend_data) & 0xffffffff
    iend = struct.pack("!I", len(iend_data)) + b'IEND' + iend_data + struct.pack("!I", iend_crc)
    
    with open(filename, 'wb') as f:
        f.write(png_magic + ihdr + idat + iend)

out_dir = "app/src/main/res/drawable-nodpi"
os.makedirs(out_dir, exist_ok=True)

names = [
    "icon_multicolor.png",
    "icon_red.png",
    "icon_green.png",
    "icon_blue.png",
    "icon_orange.png",
    "icon_gold.png"
]

for name in names:
    create_transparent_png(os.path.join(out_dir, name))

print("Created 6 dummy PNGs.")
