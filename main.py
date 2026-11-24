#!/usr/bin/env python3
"""news-23 b145 numbers-led: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.
Stdlib only (no PIL). Validates the PNG header manually with struct before copying.
"""
import hashlib
import os
import struct
import sys
import zlib

EXPECTED_SHA256 = "f5bb6b5e21bf84b342450454ac9b07fbcbca997c63e1b80db0e8ed1589f3f628"  # sha256 of entry.png
EXPECTED_SIZE = 180943  # bytes of entry.png


def fail(msg):
    print("error: " + msg, file=sys.stderr)
    return 1


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        return fail("MAKEFUN_OUTPUT_DIR is empty")
    out_dir_abs = os.path.abspath(out_dir)
    if os.path.isfile(out_dir_abs):
        return fail("MAKEFUN_OUTPUT_DIR is a file: " + out_dir)
    if out_dir_abs == here or out_dir_abs.startswith(here + os.sep):
        return fail("MAKEFUN_OUTPUT_DIR must be outside the repo")
    if not os.path.isfile(src):
        return fail("entry.png not found next to main.py")
    with open(src, "rb") as f:
        data = f.read()
    if len(data) < 10000:
        return fail("entry.png too small: %d bytes" % len(data))
    if len(data) > 1024 * 1024:
        return fail("entry.png over 1 MiB: %d bytes" % len(data))
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return fail("bad PNG signature")
    # First chunk must be IHDR, 13 bytes, 1024x1024, bit depth 8, colour type 2/6.
    if len(data) < 33:
        return fail("PNG truncated before IHDR")
    ihdr_len = struct.unpack(">I", data[8:12])[0]
    ihdr_type = data[12:16]
    if ihdr_len != 13 or ihdr_type != b"IHDR":
        return fail("first chunk is not a 13-byte IHDR")
    w, h, depth, ctype, comp, filt, inter = struct.unpack(">IIBBBBB", data[16:29])
    if (w, h) != (1024, 1024):
        return fail("expected 1024x1024, got %dx%d" % (w, h))
    if depth != 8 or ctype not in (2, 6):
        return fail("unexpected bit depth %d / colour type %d" % (depth, ctype))
    if comp != 0 or filt != 0 or inter != 0:
        return fail("unexpected compression/filter/interlace flags")
    ihdr_crc = struct.unpack(">I", data[29:33])[0]
    if zlib.crc32(data[12:29]) & 0xFFFFFFFF != ihdr_crc:
        return fail("IHDR CRC mismatch")
    # Walk chunks: CRC each, IDAT payloads non-empty (total >= 1000 bytes),
    # IEND 0-byte must be the last chunk with no trailing data.
    pos = 33
    idat_total = 0
    seen_iend = False
    while pos + 8 <= len(data):
        clen = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        if pos + 12 + clen > len(data):
            return fail("truncated chunk " + ctype.decode("latin1", "replace"))
        crc_stored = struct.unpack(">I", data[pos + 8 + clen:pos + 12 + clen])[0]
        if zlib.crc32(data[pos + 4:pos + 8 + clen]) & 0xFFFFFFFF != crc_stored:
            return fail("CRC mismatch in chunk " + ctype.decode("latin1", "replace"))
        if ctype == b"IDAT":
            if clen == 0:
                return fail("empty IDAT chunk")
            idat_total += clen
        if ctype == b"IEND":
            if clen != 0:
                return fail("IEND must be 0 bytes")
            if pos + 12 != len(data):
                return fail("trailing data after IEND")
            seen_iend = True
            break
        pos += 12 + clen
    if not seen_iend:
        return fail("no IEND chunk")
    if idat_total < 1000:
        return fail("IDAT payload too small: %d bytes" % idat_total)
    sha = hashlib.sha256(data).hexdigest()
    if EXPECTED_SHA256 and sha != EXPECTED_SHA256:
        return fail("sha256 mismatch: got %s" % sha)
    if EXPECTED_SIZE and len(data) != EXPECTED_SIZE:
        return fail("size mismatch: got %d" % len(data))
    os.makedirs(out_dir_abs, exist_ok=True)
    dst = os.path.join(out_dir_abs, "entry.png")
    if os.path.abspath(dst) == os.path.abspath(src):
        return fail("output would overwrite the source")
    with open(dst, "wb") as f:
        f.write(data)
    with open(dst, "rb") as f:
        check = f.read()
    if check != data:
        return fail("output is not byte-identical to source")
    print("wrote %s (%d bytes, sha256 %s)" % (dst, len(data), sha))
    return 0


if __name__ == "__main__":
    sys.exit(main())
