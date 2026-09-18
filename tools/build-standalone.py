#!/usr/bin/env python3
"""Inline the SheetJS bundle into index.html so the page works with no network.

Usage: python3 tools/build-standalone.py <path/to/xlsx.full.min.js> [out.html]

The published page loads SheetJS from cdnjs and degrades gracefully when that is
blocked. A standalone copy is for running the tool from disk on a network that
blocks CDNs, which is the common case behind a corporate proxy.
"""
import io, re, sys, os

SRC = os.path.join(os.path.dirname(__file__), "..", "index.html")
TAG = '<script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>'

def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    lib = io.open(sys.argv[1], encoding="utf-8").read()
    out = sys.argv[2] if len(sys.argv) > 2 else "Testfall-Schmiede.html"

    page = io.open(SRC, encoding="utf-8").read()
    if TAG not in page:
        sys.exit("The CDN script tag was not found in index.html — check the version pin.")
    if "</script" in lib:
        sys.exit("The library contains a closing script tag and cannot be inlined verbatim.")

    page = page.replace(TAG, "<script>\n/* SheetJS, inlined so this file needs no network */\n" + lib + "\n</script>", 1)
    # a standalone file is opened directly, so it carries its own document shell
    page = ('<!doctype html>\n<html lang="de">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
            '<style>:root{color-scheme:light}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n'
            + page + "\n</head>\n<body></body>\n</html>\n")
    io.open(out, "w", encoding="utf-8").write(page)
    print("wrote %s (%.1f KB)" % (out, os.path.getsize(out) / 1024))

main()
