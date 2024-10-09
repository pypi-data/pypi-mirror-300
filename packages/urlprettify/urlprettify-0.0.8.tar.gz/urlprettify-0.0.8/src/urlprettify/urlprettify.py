"""
Convert URL to reasonable format 
"""

import re
from enum import Flag, auto


class Conversion(Flag):
    """
    Conversion flags
    """
    NO_PREFIX = auto()      # Remove scheme prefix
    NO_SUFFIX = auto()      # Remove trailing suffix (port, path)
    NO_BRACES = auto()      # Remove trailing description in braces


def prettify(url: str, conversion: Conversion = Conversion.NO_BRACES
             | Conversion.NO_PREFIX | Conversion.NO_SUFFIX) -> str:
    """
    Prettify url with conversions

    Arguments:
        url -- source URL
        conversion -- conversions to apply (default - all)

    Returns:
        Pretty URL after conversions
    """

    pretty_url = url.rstrip()
    if pretty_url == '':
        return ''

    pretty_url = re.sub(r' ', '', pretty_url)
    pretty_url = re.sub(r';', '', pretty_url)

    if Conversion.NO_PREFIX in conversion:
        pretty_url = re.sub(r'^[hH].*\/\/', '', pretty_url)

    pretty_url = re.sub(r'\[\:\]', ':', pretty_url)
    pretty_url = re.sub(r'\[\.\]', '.', pretty_url)
    pretty_url = re.sub(r'\|\.\|', '.', pretty_url)
    pretty_url = re.sub(r'\|\.\]', '.', pretty_url)
    pretty_url = re.sub(r'\[\.\|', '.', pretty_url)
    pretty_url = re.sub(r'\[\]', '.', pretty_url)
    pretty_url = re.sub(r'\[\.J', '.', pretty_url)
    pretty_url = re.sub(r'\[\.\[', '.', pretty_url)
    pretty_url = re.sub(r'\.$', '', pretty_url)

    if Conversion.NO_SUFFIX in conversion:
        pretty_url = re.sub(r'(\w)\/.*$', r'\1', pretty_url)
        pretty_url = re.sub(r'(\w\:\d{1-5}).?$', r'\1', pretty_url)
        pretty_url = re.sub(r'%2F.*$', '', pretty_url)

    if Conversion.NO_BRACES in conversion:
        pretty_url = re.sub(r'\(.*\)$', '', pretty_url)
        pretty_url = re.sub(r'<(\w*)>', r'\1', pretty_url)

    pretty_url = re.sub(r'^h.*p(s)?\:\/\/', r'http\1://', pretty_url)

    return pretty_url
