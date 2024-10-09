import urllib.request
from unittest import TestCase


class SSLTest(TestCase):
    def test_01_imip_dh_key_too_small(self):
        import requests
        import ssl
        # ssl._create_default_https_context = ssl._create_unverified_context
        # requests.get('https://imip.midea.com/', contextlib=ssl._create_unverified_context())
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_1)
        context.options |= ssl.TLSVersion.TLSv1_1
        context.options |= ssl.OP_NO_COMPRESSION
        # context.minimum_version = ssl.TLSVersion.TLSv1_1
        # context.security_level = 1
        # context.verify_mode = ssl.CERT_REQUIRED
        # context.check_hostname = True
        # context.load_default_certs()

        context.set_ciphers('DEFAULT@SECLEVEL=1')
        resp = urllib.request.urlopen('https://imip.midea.com/', context=context)
        print(resp.status_code)
        print(resp.read().decode())

    def test_02_xxx(self):
        """

import requests
import urllib3
urllib3.disable_warnings()
urllib3.util.ssl_.DEFAULT_CIPHERS = 'DEFAULT@SECLEVEL=1'
resp = requests.get('https://imip.midea.com')
print(resp.status_code)
print(resp.content.decode())
        :return:
        """
        import requests
        import urllib3
        urllib3.disable_warnings()
        urllib3.util.ssl_.DEFAULT_CIPHERS = 'DEFAULT@SECLEVEL=1'
        resp = requests.get('https://imip.midea.com')
        print(resp.status_code)
        print(resp.content.decode())
