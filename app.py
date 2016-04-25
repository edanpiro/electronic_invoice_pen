# -*- coding: utf-8 -*-

import os

from client import Client
from models import Invoice

client = Client('20600247736MODDATOS', 'MODDATOS', debug=True)

file_name = '20600247736-01-F017-00004579'

data = {
    'lines': [
        {
            'quantity': 1.000,
            'amount': 123.12,
            'description': 'product description',
            'price': 123.12,
            'tax_percentage': 18.00,
            'tax_amount': 9958.10
        }
    ],
    'file_name': file_name,
    'digest_value': '123',
    'voucher_number': 'F017-0004579', # number document
    'issue_date': '2016-04-23', # date invoice
    'currency': 'PEN',
    'document_additional': [
        {
            'id': '000',
            'type_code': 05,
        }
    ],
    'company': {
        'ruc': '20600247736',
        'name': 'PYPELAB S.A.C',
        'address': 'PLG PARINACOCHAS NRO. 530 DPTO. 1 (CRUCE CON BAUSATE MEZA)LIMA - LIMA - LA VICTORIA'
    },
    'customer': {
        'ruc': '20175459902',
        'name': 'SEMINARIUM PERU S.A.',
        'type_document': '6',
        'address': 'AV. ROOSEVELT-EX REP DE PAN NRO. 6435LIMA - LIMA - MIRAFLORES',
    },
    'aditional_data': [
        {
            'code': '01',
            'value': '2016-04-28'
        }
    ],
    'catalog': [ # catalog N° 14 sunat
        {
            'code': '1001',
            'mount': 5530.31
        },
        {
            'code': '1002',
            'mount': 0.00
        },
        {
            'code': '1003',
            'mount': 0.00
        },
        {
            'code': '1004',
            'mount': 0.00
        }
    ]
}
doc = Invoice(data, file_name, client)
print doc.process()
