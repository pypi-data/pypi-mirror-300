"""
Tests for urlprettify
"""

import unittest
from src import urlprettify


class TestPrettifyFunction(unittest.TestCase):
    """
    Tests for urlprettify.prettify function
    """

    def test_prettify_empty(self):
        """
        Empty string test
        """
        self.assertEqual(urlprettify.prettify(""), "")


    def test_prettify_prefix(self):
        """
        Prefix tests
        """
        self.assertEqual(urlprettify.prettify("hxxp[:]//127.0.0.1/test.php"), "127.0.0.1")
        self.assertEqual(urlprettify.prettify("hxxp[:L//127.0.0.1/test.php"), "127.0.0.1")
        self.assertEqual(urlprettify.prettify("htttPs://ddd[.]ru"), "ddd.ru")
        self.assertEqual(urlprettify.prettify("htttP://ddd[.]ru", urlprettify.Conversion.NO_PREFIX), "ddd.ru")


    def test_prettify_suffix(self):
        """
        Suffix tests
        """
        self.assertEqual(urlprettify.prettify("127.0.0.1/test.php"), "127.0.0.1")
        self.assertEqual(urlprettify.prettify("127.0.0.1[:]4000"), "127.0.0.1")
        self.assertEqual(urlprettify.prettify("hxxp[:]//127.0.0.1[:]4000", urlprettify.Conversion.NO_SUFFIX), "http://127.0.0.1")
        self.assertEqual(urlprettify.prettify("hxxps[:]//127.0.0.1[:]4000", urlprettify.Conversion.NO_SUFFIX), "https://127.0.0.1")


    def test_prettify_braces(self):
        """
        Braces tests
        """
        self.assertEqual(urlprettify.prettify("e.gs.thc[.]org (213.171.212[.]212)"), "e.gs.thc.org")
        self.assertEqual(urlprettify.prettify("hxxp[:]//127.0.0.1[:]4000 (some info)", urlprettify.Conversion.NO_BRACES), "http://127.0.0.1:4000")
        self.assertEqual(urlprettify.prettify("gcp[.]pagaelrescate[.]<url>; "), "gcp.pagaelrescate.url")

    def test_prettify_examples(self):
        """
        Examples test
        """
        self.assertEqual(urlprettify.prettify('hxxps[:]//45[.] 143[.] 166[.] 100[:]52336/'), '45.143.166.100:52336')
        self.assertEqual(urlprettify.prettify('hxxps[:]//control-issue[.]net/?category_sports/ncaa/big-5/villanova/scamles;'), 'control-issue.net')
        self.assertEqual(urlprettify.prettify('hxxps[:]//45[.]140[.]19[.]100/;'), '45.140.19.100')
        self.assertEqual(urlprettify.prettify('hxxps[:]//45[.]131[.]46[.]228/.'), '45.131.46.228')
        self.assertEqual(urlprettify.prettify('hxxp[:]//inforussia[.]org[:]8080'), 'inforussia.org:8080')
        self.assertEqual(urlprettify.prettify('hxxps[:]//support[.]petition-change[.]org/unicorn;'), 'support.petition-change.org')
        self.assertEqual(urlprettify.prettify('hxxps[:]//yandex-drive[.]petition-change[.]org/file_preview/commecrial_list.pdf; '), 'yandex-drive.petition-change.org')
        self.assertEqual(urlprettify.prettify('hxxps[:]//213[.]183[.]54[.]123'), '213.183.54.123')
        self.assertEqual(urlprettify.prettify('hxxp [: ]//hfs [. ] lll inux [. ] com[: ] 7845/scdsshfk;'), "hfs.lllinux.com:7845")


if __name__ == '__main__':
    unittest.main()
