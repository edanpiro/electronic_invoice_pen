# coding: utf-8
from jinja2 import Template, FileSystemLoader, Environment

loader = FileSystemLoader('./templates')
env = Environment(loader=loader)


class Document(object):

    template_name = ''

    def __init__(self, data):
        self._data = data
        self._xml = None

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

    def process(self):
        """
        implement soap connection here
        save result in _result attribute
        """

    def send(self):
        self.validate()
        self.sign()
        self.render()
        self.process()
        return self._xml


class Invoice(Document):

    template_name = 'invoice.xml'

    def validate(self):
        pass
