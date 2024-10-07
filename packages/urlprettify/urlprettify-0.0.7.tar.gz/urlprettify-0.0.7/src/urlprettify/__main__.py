"""
Print urlprettify package example
"""

import sys
from .urlprettify import prettify, Conversion


def main():
    """
    Main script
    """
    ugly_url = 'hxxp[:]//рgsocket[.]io[:]5000/test.php'
    pretty_url = prettify(ugly_url, Conversion.NO_PREFIX | Conversion.NO_SUFFIX | Conversion.NO_BRACES)
    print(f"Example: {ugly_url} -> {pretty_url}")
    sys.exit(0)


if __name__ == "__main__":
    main()
