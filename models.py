# -*- coding: utf-8 -*-

import base64
import os
import zipfile

from jinja2 import Template, FileSystemLoader, Environment
from lxml import etree
from signxml import xmldsig, methods


path_dir = os.path.dirname(os.path.realpath(__file__))
attach_dir = os.path.join(path_dir, 'attach')
loader = FileSystemLoader('./templates')
env = Environment(loader=loader)


class Document(object):

    template_name = ''

    def __init__(self, data, document_name, client):
        self._data = data
        self._xml = None
        self._document_name = document_name
        self._client = client
        self._response = None
        self._zip_path = None

    def validate(self):
        """
        implement data validation
        """
        raise NotImplementedError

    def get_filename(self):
        """
        implement filename generation by document
        """
        raise NotImplementedError

    def render(self):
        template = env.get_template(self.template_name)
        self._xml = template.render(**self._data)

    def sign(self):
        # TODO: change hardcodeed key paths to environement variables
        cert = open('cert.pem').read()
        key = open('key.pem').read()

        root = etree.fromstring(self._xml.encode('ISO-8859-1'), parser=etree.XMLParser(encoding='ISO-8859-1'))
        signed_root = xmldsig(root, digest_algorithm='sha1').sign(algorithm='rsa-sha1', key=key, cert=cert)
        self._xml = etree.tostring(signed_root, encoding='ISO-8859-1')

        print (xmldsig(signed_root).verify(require_x509=True, x509_cert=cert,
                                           ca_pem_file=key, ca_path=None,
                                           hmac_key=None, validate_schema=True,
                                           parser=None, uri_resolver=None,
                                           id_attribute=None))

    def prepare_zip(self):
        self._zip_filename = '{}.zip'.format(self._document_name)
        zf = zipfile.ZipFile(self._zip_filename, mode='w', compression=zipfile.ZIP_DEFLATED)
        nx = '{}{}'.format(self._document_name, '.xml')
        zf.writestr(nx, self._xml)
        zf.close()
        self._zip_path = os.path.join(path_dir, self._zip_filename)

    def send(self):
        with open(self._zip_path, 'rb') as zf:
            encoded_content = base64.b64encode(zf.read())
            self._response = self._client.send_bill(self._zip_filename, encoded_content)

    def process_response(self):
        # save in disk response content
        if self._response is not None:
            response_data = self._response['applicationResponse']
            decoded_response_content = base64.b64decode(response_data)
            zip_file = open('response.zip', 'w')  # TODO: generate this filename
            zip_file.write(decoded_response_content)
            zip_file.close()

    def process(self):
        self.validate()
        self.render()
        self.sign()
        self.prepare_zip()
        self.send()
        self.process_response()
        return self._response


class Invoice(Document):

    template_name = 'invoice.xml'

    def validate(self):
        pass
