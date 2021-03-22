#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, print_function, unicode_literals

import sys, os, tempfile, logging
from pathlib import Path
from typing import Union

if sys.version_info >= (3,):
    import urllib.request as urllib2
    import urllib.parse as urlparse
else:
    import urllib2
    import urlparse


def get_filename(url, dest=None, filename: Union[str, Path] = None):
    scheme, netloc, path, query, fragment = urlparse.urlsplit(url)
    if filename is None:
        filename = os.path.basename(path)
    if not filename:
        filename = "downloaded.file"
    if dest:
        filename = os.path.join(dest, filename)
    return Path(filename)


def download_file(url, dest=None, filename=None):
    """
    Download and save a file specified by url to dest directory,

    Inspired by:
    PabloG, Stan and Steve Barnes
    https://stackoverflow.com/questions/22676/how-do-i-download-a-file-over-http-using-python?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
    """
    u = urllib2.urlopen(url)

    filename = get_filename(url, dest, filename)

    with open(filename, "wb") as f:
        meta = u.info()
        meta_func = meta.getheaders if hasattr(meta, "getheaders") else meta.get_all
        meta_length = meta_func("Content-Length")
        file_size = None
        if meta_length:
            file_size = int(meta_length[0])
        print("Downloading: {0} Bytes: {1}".format(url, file_size))

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)

            status = "{0:16}".format(file_size_dl)
            if file_size:
                status += "   [{0:6.2f}%]".format(file_size_dl * 100 / file_size)
            status += chr(13)
            print(status, end="")


def is_url(url):
    """
    Check if string is url. From django.
    :param url:
    :return:
    """
    import re

    regex = re.compile(
        r"^(?:http|ftp)s?://"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )

    return re.match(regex, str(url)) is not None
