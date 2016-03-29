# coding: utf-8

import os
import zipfile
from lxml import etree
from jinja2 import Template, FileSystemLoader, Environment
from signxml import xmldsig, methods


path_dir = os.path.dirname(os.path.realpath(__file__))
attach_dir = os.path.join(path_dir, 'attach')
loader = FileSystemLoader('./templates')
env = Environment(loader=loader)


class Document(object):

    template_name = ''

    def __init__(self, data, document_name):
        self._data = data
        self._xml = None
        self._document_name = document_name

    def validate(self):
        """
        implement data validation
        """
        raise NotImplementedError

    def render(self):
        template = env.get_template(self.template_name)
        self._xml = template.render(**self._data)

    def sign(self):
        """
        implement signature process
        """

    def out_zip(self):
        cert = open('cert.pem').read()
        key = open('key.pem').read()
        zf = zipfile.ZipFile('{}.zip'.format(self._document_name), mode='w', compression=zipfile.ZIP_DEFLATED)
        file_xml = os.path.join(attach_dir, self._document_name)
        root = etree.fromstring(self._xml.encode('ISO-8859-1'), parser=etree.XMLParser(encoding='ISO-8859-1'))
        signed_root = xmldsig(root, digest_algorithm='sha1').sign(method=methods.enveloped,
                                                                  algorithm='rsa-sha1',
                                                                  passphrase=None,
                                                                  key=key, cert=cert)
        self._xml = etree.tostring(root)
        # signed_root = etree.tostring()
        # verified_data = xmldsig(signed_root).verify()

        print self._xml
        zf.writestr(self._document_name, self._xml)
        # file_xml = os.path.join(attach_dir, self._document_name)
        # zf.write(os.walk(file_xml))
        zf.close()

    def process(self):
        """
        implement soap connection here
        save result in _result attribute
        """

    def send(self):
        self.validate()
        self.sign()
        self.render()
        # self.out_xml()
        self.out_zip()
        self.process()
        # return self._xml


class Invoice(Document):

    template_name = 'invoice.xml'

    def validate(self):
        pass
